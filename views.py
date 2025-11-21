from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Movie, Show, Booking
from .serializers import (
    UserSignupSerializer, UserLoginSerializer, MovieSerializer,
    ShowSerializer, BookingSerializer, BookSeatSerializer
)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        request_body=UserSignupSerializer,
        responses={
            201: openapi.Response('User created successfully', UserSignupSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        """
        Register a new user
        """
        try:
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': 'User registered successfully',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                'Login successful',
                examples={
                    'application/json': {
                        'message': 'Login successful',
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'user': {'id': 1, 'username': 'john_doe'}
                    }
                }
            ),
            401: 'Invalid credentials'
        }
    )
    def post(self, request):
        """
        Authenticate user and return JWT tokens
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Login successful',
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'id': user.id,
                            'username': user.username
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieListView(generics.ListAPIView):
    """
    List all movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class MovieShowsView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        responses={
            200: ShowSerializer(many=True),
            404: 'Movie not found'
        }
    )
    def get(self, request, movie_id):
        """
        List all shows for a specific movie
        """
        try:
            movie = Movie.objects.get(id=movie_id)
            shows = Show.objects.filter(movie=movie)
            serializer = ShowSerializer(shows, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookSeatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=BookSeatSerializer,
        responses={
            201: openapi.Response('Booking successful', BookingSerializer),
            400: 'Bad Request',
            404: 'Show not found'
        }
    )
    def post(self, request, show_id):
        """
        Book a seat for a show
        """
        try:
            serializer = BookSeatSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            seat_number = serializer.validated_data['seat_number']
            
            try:
                show = Show.objects.get(id=show_id)
            except Show.DoesNotExist:
                return Response({'error': 'Show not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Validate seat number
            if seat_number > show.total_seats:
                return Response({
                    'error': f'Invalid seat number. This show has only {show.total_seats} seats.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Use transaction to prevent race conditions
            with transaction.atomic():
                # Check if seat is already booked
                existing_booking = Booking.objects.filter(
                    show=show,
                    seat_number=seat_number,
                    status='booked'
                ).select_for_update().exists()
                
                if existing_booking:
                    return Response({
                        'error': f'Seat {seat_number} is already booked for this show.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Check if show is full
                booked_seats = Booking.objects.filter(
                    show=show,
                    status='booked'
                ).count()
                
                if booked_seats >= show.total_seats:
                    return Response({
                        'error': 'This show is fully booked.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    seat_number=seat_number,
                    status='booked'
                )
                
                booking_serializer = BookingSerializer(booking)
                return Response({
                    'message': 'Seat booked successfully',
                    'booking': booking_serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CancelBookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: 'Booking cancelled successfully',
            403: 'Forbidden',
            404: 'Booking not found'
        }
    )
    def post(self, request, booking_id):
        """
        Cancel a booking
        """
        try:
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Security check: user can only cancel their own booking
            if booking.user != request.user:
                return Response({
                    'error': 'You can only cancel your own bookings.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Check if already cancelled
            if booking.status == 'cancelled':
                return Response({
                    'error': 'This booking is already cancelled.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Cancel the booking
            booking.status = 'cancelled'
            booking.save()
            
            return Response({
                'message': 'Booking cancelled successfully',
                'booking_id': booking.id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyBookingsView(generics.ListAPIView):
    """
    List all bookings for the logged-in user
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
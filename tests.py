from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import Movie, Show, Booking


class BookingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Create test movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            duration_minutes=120
        )
        
        # Create test show
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name='Screen 1',
            date_time=datetime.now() + timedelta(days=1),
            total_seats=10
        )
        
        # Get JWT token
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_signup(self):
        """Test user registration"""
        response = self.client.post('/signup/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login(self):
        """Test user login"""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_book_seat(self):
        """Test booking a seat"""
        response = self.client.post(f'/shows/{self.show.id}/book/', {
            'seat_number': 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_prevent_double_booking(self):
        """Test that double booking is prevented"""
        # Book seat 1
        self.client.post(f'/shows/{self.show.id}/book/', {
            'seat_number': 1
        })
        
        # Try to book seat 1 again
        response = self.client.post(f'/shows/{self.show.id}/book/', {
            'seat_number': 1
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_prevent_overbooking(self):
        """Test that overbooking is prevented"""
        # Book all seats
        for i in range(1, 11):
            self.client.post(f'/shows/{self.show.id}/book/', {
                'seat_number': i
            })
        
        # Create another user
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        client2 = APIClient()
        response = client2.post('/login/', {
            'username': 'testuser2',
            'password': 'testpass123'
        })
        client2.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        
        # Try to book another seat (should fail)
        response = client2.post(f'/shows/{self.show.id}/book/', {
            'seat_number': 5
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cancel_booking(self):
        """Test cancelling a booking"""
        # Book a seat
        response = self.client.post(f'/shows/{self.show.id}/book/', {
            'seat_number': 1
        })
        booking_id = response.data['booking']['id']
        
        # Cancel the booking
        response = self.client.post(f'/bookings/{booking_id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify booking is cancelled
        booking = Booking.objects.get(id=booking_id)
        self.assertEqual(booking.status, 'cancelled')
    
    def test_user_cannot_cancel_others_booking(self):
        """Test that a user cannot cancel another user's booking"""
        # Book a seat with first user
        response = self.client.post(f'/shows/{self.show.id}/book/', {
            'seat_number': 1
        })
        booking_id = response.data['booking']['id']
        
        # Create and login as second user
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        client2 = APIClient()
        response = client2.post('/login/', {
            'username': 'testuser2',
            'password': 'testpass123'
        })
        client2.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        
        # Try to cancel first user's booking
        response = client2.post(f'/bookings/{booking_id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_my_bookings(self):
        """Test retrieving user's bookings"""
        # Create two bookings
        self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 1})
        self.client.post(f'/shows/{self.show.id}/book/', {'seat_number': 2})
        
        # Get bookings
        response = self.client.get('/my-bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
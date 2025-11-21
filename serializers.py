from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Movie, Show, Booking


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes', 'created_at']
        read_only_fields = ['id', 'created_at']


class ShowSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Show
        fields = ['id', 'movie', 'movie_title', 'screen_name', 'date_time', 
                  'total_seats', 'available_seats', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    movie_title = serializers.CharField(source='show.movie.title', read_only=True)
    screen_name = serializers.CharField(source='show.screen_name', read_only=True)
    show_time = serializers.DateTimeField(source='show.date_time', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_username', 'show', 'movie_title', 
                  'screen_name', 'show_time', 'seat_number', 'status', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']


class BookSeatSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField(min_value=1, required=True)
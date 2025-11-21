from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.movie.title} - {self.screen_name} - {self.date_time}"
    
    @property
    def available_seats(self):
        booked_count = self.bookings.filter(status='booked').count()
        return self.total_seats - booked_count
    
    class Meta:
        ordering = ['date_time']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seat_number = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return f"{self.user.username} - {self.show} - Seat {self.seat_number}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['show', 'seat_number', 'status']
        indexes = [
            models.Index(fields=['show', 'seat_number', 'status']),
        ]
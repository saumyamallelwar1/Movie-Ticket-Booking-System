from django.contrib import admin
from .models import Movie, Show, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration_minutes', 'created_at']
    search_fields = ['title']
    list_filter = ['created_at']


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'screen_name', 'date_time', 'total_seats', 'available_seats']
    search_fields = ['movie__title', 'screen_name']
    list_filter = ['date_time', 'screen_name']
    date_hierarchy = 'date_time'
    
    def available_seats(self, obj):
        return obj.available_seats
    available_seats.short_description = 'Available Seats'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'show', 'seat_number', 'status', 'created_at']
    search_fields = ['user_username', 'showmovie_title']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
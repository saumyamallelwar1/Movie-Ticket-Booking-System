from django.urls import path
from .views import (
    SignupView, LoginView, MovieListView, MovieShowsView,
    BookSeatView, CancelBookingView, MyBookingsView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', MovieShowsView.as_view(), name='movie-shows'),
    path('shows/<int:show_id>/book/', BookSeatView.as_view(), name='book-seat'),
    path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
]
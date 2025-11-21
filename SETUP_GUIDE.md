# Complete Setup Guide

## Step-by-Step Setup Instructions

### Step 1: Create Project Structure

Create the following directory structure:


movie-ticket-booking/
├── movie_booking/
│   ├── __init__.py (empty file)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── booking/
│   ├── __init__.py (empty file)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore


### Step 2: Install Dependencies

bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt


### Step 3: Run Migrations

bash
python manage.py makemigrations
python manage.py migrate


### Step 4: Create Superuser (Optional)

bash
python manage.py createsuperuser
# Follow the prompts to create admin user


### Step 5: Start Server

bash
python manage.py runserver


### Step 6: Access the Application

- *Swagger Documentation*: http://127.0.0.1:8000/swagger/
- *Admin Panel*: http://127.0.0.1:8000/admin/
- *API Base URL*: http://127.0.0.1:8000/

## Testing the API

### Method 1: Using Swagger UI (Recommended)

1. Open http://127.0.0.1:8000/swagger/
2. Find the /signup/ endpoint
3. Click "Try it out"
4. Enter user details and execute
5. Find the /login/ endpoint
6. Login with your credentials
7. Copy the access token from response
8. Click "Authorize" button at top
9. Enter: Bearer <your-token>
10. Now you can test all protected endpoints

### Method 2: Using cURL

bash
# 1. Signup
curl -X POST http://127.0.0.1:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'

# 2. Login
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Save the access token from response

# 3. Get Movies (no auth needed)
curl http://127.0.0.1:8000/movies/

# 4. Book a seat (needs auth)
curl -X POST http://127.0.0.1:8000/shows/1/book/ \
  -H "Authorization: Bearer <your-access-token>" \
  -H "Content-Type: application/json" \
  -d '{"seat_number": 5}'

# 5. View my bookings
curl http://127.0.0.1:8000/my-bookings/ \
  -H "Authorization: Bearer <your-access-token>"

# 6. Cancel booking
curl -X POST http://127.0.0.1:8000/bookings/1/cancel/ \
  -H "Authorization: Bearer <your-access-token>"


### Method 3: Using Postman

1. Import the following as a collection:
   - Base URL: http://127.0.0.1:8000
   - Add endpoints as per API documentation

2. For protected endpoints:
   - Go to Authorization tab
   - Select Type: Bearer Token
   - Paste your access token

## Adding Test Data

### Using Django Admin

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser
3. Add Movies and Shows

### Using Django Shell

bash
python manage.py shell


python
from booking.models import Movie, Show
from datetime import datetime, timedelta

# Create movies
movie1 = Movie.objects.create(title="Inception", duration_minutes=148)
movie2 = Movie.objects.create(title="The Dark Knight", duration_minutes=152)
movie3 = Movie.objects.create(title="Interstellar", duration_minutes=169)

# Create shows
Show.objects.create(
    movie=movie1,
    screen_name="Screen 1",
    date_time=datetime.now() + timedelta(days=1, hours=3),
    total_seats=50
)

Show.objects.create(
    movie=movie1,
    screen_name="Screen 2",
    date_time=datetime.now() + timedelta(days=1, hours=6),
    total_seats=40
)

Show.objects.create(
    movie=movie2,
    screen_name="Screen 1",
    date_time=datetime.now() + timedelta(days=2, hours=4),
    total_seats=60
)

print("Test data created successfully!")


## Running Tests

bash
# Run all tests
python manage.py test

# Run tests with verbose output
python manage.py test --verbosity=2

# Run specific test
python manage.py test booking.tests.BookingTestCase.test_book_seat


## Common Issues and Solutions

### Issue 1: ModuleNotFoundError

*Solution*: Make sure you've activated the virtual environment and installed all dependencies.

bash
pip install -r requirements.txt


### Issue 2: No such table errors

*Solution*: Run migrations

bash
python manage.py makemigrations
python manage.py migrate


### Issue 3: JWT token not working

*Solution*: Make sure you're including "Bearer " before the token:


Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...


### Issue 4: CSRF token errors

*Solution*: CSRF is disabled for API endpoints. Make sure you're using the correct headers.

## Production Deployment Checklist

Before deploying to production:

- [ ] Set DEBUG = False in settings.py
- [ ] Change SECRET_KEY to a secure random value
- [ ] Use environment variables for sensitive data
- [ ] Configure PostgreSQL or MySQL database
- [ ] Set up proper static file serving
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure CORS if needed
- [ ] Use gunicorn or uwsgi as WSGI server
- [ ] Set up Redis for caching (optional)
- [ ] Configure backup strategy

## Support

For any issues or questions, please refer to:
- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- JWT Documentation: https://django-rest-framework-simplejwt.readthedocs.io/
# Movie Ticket Booking System

A REST API built with Django and Django REST Framework for managing movie ticket bookings with JWT authentication.

## 🚀 Features

- User authentication with JWT tokens
- Movie and show management
- Seat booking with double-booking prevention
- Booking cancellation
- Comprehensive API documentation with Swagger
- Input validation and error handling
- Security best practices implemented
- Unit tests for booking logic

## 📋 Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## 🛠 Installation & Setup

### 1. Clone the repository

bash
git clone <your-repo-url>
cd movie-ticket-booking


### 2. Create and activate virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate


### 3. Install dependencies

bash
pip install -r requirements.txt


### 4. Project Structure

Create the following structure:


movie_booking/
├── movie_booking/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── booking/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
├── manage.py
├── requirements.txt
└── README.md


### 5. Apply migrations

bash
python manage.py makemigrations
python manage.py migrate


### 6. Create superuser (optional)

bash
python manage.py createsuperuser


### 7. Run the development server

bash
python manage.py runserver


The server will start at http://127.0.0.1:8000/

## 📚 API Documentation

Access the Swagger documentation at: *http://127.0.0.1:8000/swagger/*

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Register a new user or login
2. Copy the access token from the response
3. In Swagger UI, click the *Authorize* button
4. Enter: Bearer <your-access-token>
5. Click *Authorize*

### Example using cURL:

bash
# Include token in header
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:8000/my-bookings/


## 🎯 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /signup/ | Register a new user | No |
| POST | /login/ | Login and get JWT token | No |

### Movies & Shows

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /movies/ | List all movies | No |
| GET | /movies/<id>/shows/ | List all shows for a movie | No |

### Bookings

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /shows/<id>/book/ | Book a seat | Yes |
| POST | /bookings/<id>/cancel/ | Cancel a booking | Yes |
| GET | /my-bookings/ | List user's bookings | Yes |

## 📝 Usage Examples

### 1. Register a User

bash
curl -X POST http://127.0.0.1:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'


### 2. Login

bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'


*Response:*
json
{
  "message": "Login successful",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe"
  }
}


### 3. List Movies

bash
curl http://127.0.0.1:8000/movies/


### 4. Book a Seat

bash
curl -X POST http://127.0.0.1:8000/shows/1/book/ \
  -H "Authorization: Bearer <your-access-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "seat_number": 5
  }'


### 5. View My Bookings

bash
curl http://127.0.0.1:8000/my-bookings/ \
  -H "Authorization: Bearer <your-access-token>"


### 6. Cancel a Booking

bash
curl -X POST http://127.0.0.1:8000/bookings/1/cancel/ \
  -H "Authorization: Bearer <your-access-token>"


## 🧪 Running Tests

bash
python manage.py test booking


## 🗄 Adding Sample Data

You can add sample data through the Django admin panel or Django shell:

### Using Django Admin

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Add Movies, Shows, and Bookings

### Using Django Shell

bash
python manage.py shell


python
from booking.models import Movie, Show
from datetime import datetime, timedelta

# Create a movie
movie = Movie.objects.create(
    title="Inception",
    duration_minutes=148
)

# Create a show
Show.objects.create(
    movie=movie,
    screen_name="Screen 1",
    date_time=datetime.now() + timedelta(days=1),
    total_seats=50
)

##Screenshot
![WhatsApp Image 2025-11-21 at 11 08 26_dc8dc317](https://github.com/user-attachments/assets/431ac3cd-ce94-49d3-b374-75d1dc775e40)
![WhatsApp Image 2025-11-21 at 11 08 26_c0891010](https://github.com/user-attachments/assets/ea8111c1-1403-4b1b-8555-0037d00f45b3)
![WhatsApp Image 2025-11-21 at 11 08 27_89dd6b9f](https://github.com/user-attachments/assets/db52df5c-2550-4bdb-8dfe-f0fcd5de8414)
![WhatsApp Image 2025-11-21 at 11 08 27_16daeef1](https://github.com/user-attachments/assets/a84ae185-7153-4f93-b607-947bfac2ef3f)
![WhatsApp Image 2025-11-21 at 11 08 28_55c435a8](https://github.com/user-attachments/assets/7346303d-d893-49c5-a6c8-aa2693ed6c84)
![WhatsApp Image 2025-11-21 at 11 08 28_ff2ae27c](https://github.com/user-attachments/assets/671e5742-fe3e-4fe6-b2da-4cc022cd85f4)
![WhatsApp Image 2025-11-21 at 11 08 29_5aa452b7](https://github.com/user-attachments/assets/67bf5bb9-4a9a-44bb-81a7-fd7f39d8f8c7)
![WhatsApp Image 2025-11-21 at 11 08 29_2896882e](https://github.com/user-attachments/assets/511412de-8176-4a9c-9b7a-b68e2fb846ff)
![WhatsApp Image 2025-11-21 at 11 08 30_c8e07d98](https://github.com/user-attachments/assets/574ea416-a466-4fbd-9e6f-19aa221dc3d0)
![WhatsApp Image 2025-11-21 at 11 08 30_961d4ea0](https://github.com/user-attachments/assets/77485df6-62b9-425d-9ba7-dd13e1d19616)

## ✅ Business Rules Implemented

- ✓ *Prevent double booking*: A seat cannot be booked twice for the same show
- ✓ *Prevent overbooking*: Bookings cannot exceed show capacity
- ✓ *Seat release on cancellation*: Cancelled bookings free up seats
- ✓ *User authorization*: Users can only cancel their own bookings
- ✓ *Seat validation*: Prevents booking seat numbers outside allowed range
- ✓ *Transaction safety*: Uses database transactions to prevent race conditions

## 🔒 Security Features

- JWT authentication for protected endpoints
- Password validation with Django validators
- User can only cancel their own bookings
- Database-level constraints for data integrity
- CSRF protection enabled
- SQL injection prevention through Django ORM

## 📦 Tech Stack

- *Backend Framework*: Django 4.2.7
- *API Framework*: Django REST Framework 3.14.0
- *Authentication*: djangorestframework-simplejwt 5.3.0
- *API Documentation*: drf-yasg 1.21.7
- *Database*: SQLite (development)

## 🐛 Error Handling

All endpoints include comprehensive error handling:

- *400 Bad Request*: Invalid input data
- *401 Unauthorized*: Missing or invalid JWT token
- *403 Forbidden*: Insufficient permissions
- *404 Not Found*: Resource doesn't exist
- *500 Internal Server Error*: Server-side errors

## 📄 License

This project is created as an assignment for Backend Developer Intern position.

## 👤 Author

 Saumya Mallelwar - Backend Developer Intern Candidate

## 🤝 Contributing

This is an assignment project. For any questions, please contact the development team.

---

*Note*: This is a development setup. For production deployment, update the following:
- Change DEBUG = False in settings.py
- Set a secure SECRET_KEY
- Configure proper database (PostgreSQL recommended)
- Set up proper static file serving
- Configure CORS if needed
- Use environment variables for sensitive data


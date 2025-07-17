# Growdigo Django Backend

This is the Django backend for the Growdigo application that handles user registration and stores data in PostgreSQL.

## Prerequisites

1. **Python 3.8+** installed on your system
2. **PostgreSQL** installed and running on localhost:5432
3. **pip** (Python package installer)

## Database Setup

1. **Start PostgreSQL** (if not already running)
2. **Create the database**:
   ```sql
   CREATE DATABASE growings_db;
   ```
3. **Default database credentials** (update in settings.py if different):
   - Database: `growings_db`
   - User: `postgres`
   - Password: `postgres`
   - Host: `localhost`
   - Port: `5432`

## Installation & Setup

1. **Navigate to the Django directory**:
   ```bash
   cd growings-django
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the setup script** (optional):
   ```bash
   python3 setup.py
   ```

4. **Create database migrations**:
   ```bash
   python3 manage.py makemigrations
   ```

5. **Apply migrations**:
   ```bash
   python3 manage.py migrate
   ```

6. **Create a superuser** (optional):
   ```bash
   python3 manage.py createsuperuser
   ```

## Running the Server

1. **Start the Django development server**:
   ```bash
   python3 manage.py runserver
   ```

2. **The server will run on**: http://localhost:8000

3. **API endpoints**:
   - Registration: `POST http://localhost:8000/api/register/`
   - Admin panel: http://localhost:8000/admin/

## API Usage

### User Registration

**Endpoint**: `POST /api/register/`

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response** (Success - 201):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Response** (Error - 400):
```json
{
  "message": "Registration failed",
  "errors": {
    "email": ["A user with this email already exists."]
  }
}
```

## Frontend Integration

The React frontend is configured to send registration data to:
- `http://localhost:8000/api/register/`

Make sure both servers are running:
- Django backend: `http://localhost:8000`
- React frontend: `http://localhost:3000`

## Troubleshooting

1. **Database connection issues**:
   - Check if PostgreSQL is running
   - Verify database credentials in `settings.py`
   - Ensure database `growings_db` exists

2. **CORS issues**:
   - Frontend should be running on `http://localhost:3000`
   - CORS is configured to allow requests from this origin

3. **Migration issues**:
   - Delete `migrations/` folder (except `__init__.py`)
   - Run `python3 manage.py makemigrations` again
   - Run `python3 manage.py migrate`

## Project Structure

```
growings-django/
├── growings_backend/     # Main Django project
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── users/               # Users app
│   ├── models.py        # User model
│   ├── views.py         # Registration view
│   ├── serializers.py   # API serializers
│   └── urls.py          # App URL configuration
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
└── README.md           # This file
``` 
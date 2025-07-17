# Growings Backend - Render Deployment Guide

This guide will help you deploy the Growings Django backend to Render.

## Prerequisites

1. A Render account
2. Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository contains:
- `build.sh` (build script for Render)
- `requirements.txt` (Python dependencies)
- `manage.py` (Django management script)
- Your Django project files

### 2. Create a New Web Service on Render

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name**: `growings-backend` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn growings_backend.wsgi:application`
   - **Plan**: Choose your preferred plan

### 3. Environment Variables

Add these environment variables in your Render service settings:

#### Required Variables:
- `SECRET_KEY`: A secure Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain(s), e.g., `your-app.onrender.com`

#### Database (Render will provide automatically):
- `DATABASE_URL`: Render will set this automatically when you add a PostgreSQL database

#### Optional Variables:
- `CORS_ALLOWED_ORIGINS`: Your frontend URLs
- `RAZORPAY_KEY_ID`: Your Razorpay key ID
- `RAZORPAY_KEY_SECRET`: Your Razorpay secret key
- `RAZORPAY_REGISTRATION_AMOUNT`: Registration amount in paise

### 4. Add PostgreSQL Database

1. In your Render dashboard, create a new PostgreSQL database
2. Connect it to your web service
3. Render will automatically set the `DATABASE_URL` environment variable

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues

## Local Development Setup

1. Copy `env_template.txt` to `.env`
2. Update the values in `.env` with your local configuration
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Important Notes

- The `build.sh` script will automatically run migrations and collect static files
- Make sure your `SECRET_KEY` is secure and unique
- In production, `DEBUG` should always be `False`
- The application uses WhiteNoise for static file serving
- CORS is configured to work with your frontend application

## Troubleshooting

- Check the build logs in Render for any errors
- Ensure all environment variables are set correctly
- Verify that your database is properly connected
- Check that all required dependencies are in `requirements.txt` 
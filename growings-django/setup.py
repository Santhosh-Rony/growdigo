#!/usr/bin/env python3
"""
Setup script for Growdigo Django Backend
This script will help you set up the Django project with PostgreSQL
"""

import os
import sys
import subprocess

def run_command(command, description):
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Growdigo Django Backend...")
    
    # Check if Python is available
    if not run_command("python3 --version", "Checking Python version"):
        print("❌ Python 3 is required but not found")
        return False
    
    # Install requirements
    if not run_command("pip3 install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        return False
    
    # Make migrations
    if not run_command("python3 manage.py makemigrations", "Creating database migrations"):
        print("❌ Failed to create migrations")
        return False
    
    # Run migrations
    if not run_command("python3 manage.py migrate", "Running database migrations"):
        print("❌ Failed to run migrations")
        return False
    
    # Create superuser (optional)
    print("\n📝 Create a superuser account (optional):")
    print("Run: python3 manage.py createsuperuser")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure PostgreSQL is running on localhost:5432")
    print("2. Create a database named 'growings_db'")
    print("3. Update database credentials in settings.py if needed")
    print("4. Start the Django server: python3 manage.py runserver")
    print("5. Start your React app: npm start")
    
    return True

if __name__ == "__main__":
    main() 
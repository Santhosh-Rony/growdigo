#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growings_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
import json

User = get_user_model()

def test_login_session_creation():
    """Test if login actually creates Django sessions"""
    
    print("🧪 Testing Login Session Creation")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Check existing users
    users = User.objects.all()
    print(f"Users in database: {users.count()}")
    for user in users:
        print(f"  - {user.email} (ID: {user.id})")
    
    if users.count() == 0:
        print("❌ No users found. Please create a user first.")
        return
    
    test_user = users.first()
    print(f"\n🔍 Testing with user: {test_user.email}")
    
    # Check sessions before login
    sessions_before = Session.objects.count()
    print(f"Sessions before login: {sessions_before}")
    
    # Attempt login
    login_data = {
        'email': test_user.email,
        'password': 'your_password_here'  # You'll need to set this
    }
    
    print(f"\n🔐 Attempting login...")
    response = client.post('/api/login/', login_data, content_type='application/json')
    print(f"Login response status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Login successful")
        response_data = json.loads(response.content)
        print(f"Response: {response_data}")
    else:
        print("❌ Login failed")
        print(f"Response: {response.content}")
    
    # Check sessions after login
    sessions_after = Session.objects.count()
    print(f"\nSessions after login: {sessions_after}")
    
    if sessions_after > sessions_before:
        print("✅ Session created successfully")
        # Get the session
        latest_session = Session.objects.latest('expire_date')
        session_data = latest_session.get_decoded()
        print(f"Session data: {session_data}")
        user_id = session_data.get('_auth_user_id')
        if user_id:
            print(f"Session belongs to user ID: {user_id}")
    else:
        print("❌ No session created during login")
    
    # Test session validation endpoint
    print(f"\n🔍 Testing session validation endpoint...")
    validation_response = client.get('/api/validate-session/')
    print(f"Validation response status: {validation_response.status_code}")
    
    if validation_response.status_code == 200:
        validation_data = json.loads(validation_response.content)
        print(f"✅ Session validation successful: {validation_data}")
    else:
        print(f"❌ Session validation failed: {validation_response.content}")

if __name__ == '__main__':
    test_login_session_creation()

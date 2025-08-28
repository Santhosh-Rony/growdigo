#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growings_backend.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

print('=== Debugging Session Issue ===')

# Check active sessions
active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
print(f'Total active sessions: {active_sessions.count()}')

orphaned_sessions = 0
for session in active_sessions:
    data = session.get_decoded()
    user_id = data.get('_auth_user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            print(f'✅ Session {session.session_key[:8]}... → {user.email}')
        except User.DoesNotExist:
            print(f'❌ ORPHANED Session {session.session_key[:8]}... → Deleted user ID: {user_id}')
            orphaned_sessions += 1

print(f'\nOrphaned sessions found: {orphaned_sessions}')

# Test signal import
try:
    import users.signals
    print('✅ Signals module imported successfully')
except Exception as e:
    print(f'❌ Signal import error: {e}')

# Check if apps.py ready method is working
try:
    from django.apps import apps
    users_config = apps.get_app_config('users')
    print(f'✅ Users app config: {users_config.__class__.__name__}')
except Exception as e:
    print(f'❌ App config error: {e}')

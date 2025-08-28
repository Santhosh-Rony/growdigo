from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@receiver(post_delete, sender=User)
def invalidate_user_sessions(sender, instance, **kwargs):
    """
    Signal handler to invalidate all sessions for a user when their account is deleted.
    This ensures automatic logout for all active sessions of the deleted user.
    """
    try:
        user_id = instance.id
        logger.info(f"User {instance.email} (ID: {user_id}) deleted. Invalidating all sessions.")
        
        # Get all active sessions
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        sessions_deleted = 0
        
        for session in active_sessions:
            session_data = session.get_decoded()
            # Check if this session belongs to the deleted user
            if session_data.get('_auth_user_id') == str(user_id):
                session.delete()
                sessions_deleted += 1
                logger.info(f"Deleted session {session.session_key} for user {instance.email}")
        
        logger.info(f"Invalidated {sessions_deleted} sessions for deleted user {instance.email}")
        
    except Exception as e:
        logger.error(f"Error invalidating sessions for deleted user {instance.email}: {str(e)}")

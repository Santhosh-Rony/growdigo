from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class ValidateUserSessionMiddleware:
    """
    Middleware to validate that authenticated users still exist in the database.
    If a user's account has been deleted, automatically log them out.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            try:
                # Try to fetch the user from database to ensure they still exist
                User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                # User no longer exists in database, log them out
                logger.info(f"User ID {request.user.id} no longer exists. Logging out session.")
                logout(request)
                
                # If this is an API request, return JSON response
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'message': 'Your account has been deactivated. Please contact support.',
                        'error': 'account_deactivated'
                    }, status=401)
        
        response = self.get_response(request)
        return response

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .serializers import UserRegistrationSerializer
from payments.models import PaymentTransaction
from django.utils import timezone

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Check if payment verification data is provided
        payment_data = request.data.get('payment_data')
        
        if not payment_data:
            return Response({
                'message': 'Payment verification required',
                'error': 'Payment data is missing'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify payment before creating user
        razorpay_payment_id = payment_data.get('razorpay_payment_id')
        razorpay_order_id = payment_data.get('razorpay_order_id')
        upi_id = payment_data.get('upi_id', None)  # Make UPI ID optional
        
        if not razorpay_payment_id or not razorpay_order_id:
            return Response({
                'message': 'Payment verification failed',
                'error': 'Payment details are incomplete'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user first
        user = serializer.save()
        
        # Create payment transaction
        try:
            transaction = PaymentTransaction.objects.create(
                user=user,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                amount=settings.RAZORPAY_REGISTRATION_AMOUNT / 100,  # Convert from paise
                status='captured',
                payment_method='upi',
                upi_id=upi_id
            )
            
            # Update user payment status
            user.payment_status = 'completed'
            user.razorpay_payment_id = razorpay_payment_id
            user.razorpay_order_id = razorpay_order_id
            user.payment_amount = settings.RAZORPAY_REGISTRATION_AMOUNT / 100
            user.payment_date = timezone.now()
            user.save()
            
            return Response({
                'message': 'User registered successfully with payment',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'payment_status': user.payment_status
                },
                'transaction_id': transaction.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # If payment transaction creation fails, delete the user
            user.delete()
            return Response({
                'message': 'Registration failed',
                'error': f'Payment processing error: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'message': 'Registration failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'message': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user
    user = authenticate(username=email, password=password)
    
    if user is not None:
        # Log the user in to create a session
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': 'Login unsuccessful. Please register first or check your credentials.'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout the current user by clearing their session.
    """
    logout(request)
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_session(request):
    """
    Validate if the current session is still valid.
    Returns user info if valid, 401 if invalid.
    """
    return Response({
        'message': 'Session valid',
        'user': {
            'id': request.user.id,
            'name': request.user.name,
            'email': request.user.email
        }
    }, status=status.HTTP_200_OK) 
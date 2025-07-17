import razorpay
import hmac
import hashlib
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CreateOrderSerializer, PaymentVerificationSerializer
from .models import PaymentTransaction
from users.models import User
from django.utils import timezone

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a Razorpay order for registration payment"""
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Create Razorpay order
            order_data = {
                'amount': int(serializer.validated_data['amount'] * 100),  # Convert to paise
                'currency': serializer.validated_data['currency'],
                'receipt': f"order_rcptid_{int(timezone.now().timestamp())}",
                'notes': {
                    'description': 'Growdigo Premium Registration'
                }
            }
            
            order = client.order.create(data=order_data)
            
            return Response({
                'success': True,
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'key_id': settings.RAZORPAY_KEY_ID
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    """Verify Razorpay payment signature and complete registration"""
    serializer = PaymentVerificationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Get payment data
            razorpay_order_id = serializer.validated_data['razorpay_order_id']
            razorpay_payment_id = serializer.validated_data['razorpay_payment_id']
            razorpay_signature = serializer.validated_data['razorpay_signature']
            
            # Verify signature
            text = f"{razorpay_order_id}|{razorpay_payment_id}"
            signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                text.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if signature != razorpay_signature:
                return Response({
                    'success': False,
                    'error': 'Invalid payment signature'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get payment details from Razorpay
            payment = client.payment.fetch(razorpay_payment_id)
            
            if payment['status'] == 'captured':
                # Payment successful - update user and create transaction record
                # Note: User creation will be handled in the registration view
                return Response({
                    'success': True,
                    'payment_id': razorpay_payment_id,
                    'order_id': razorpay_order_id,
                    'amount': payment['amount'] / 100,  # Convert from paise
                    'status': payment['status']
                })
            else:
                return Response({
                    'success': False,
                    'error': 'Payment not completed'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_payment_transaction(request):
    """Create payment transaction record after successful payment"""
    try:
        user_id = request.data.get('user_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        amount = request.data.get('amount')
        upi_id = request.data.get('upi_id', None)  # Make UPI ID optional
        
        user = User.objects.get(id=user_id)
        
        # Create payment transaction
        transaction = PaymentTransaction.objects.create(
            user=user,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            amount=amount,
            status='captured',
            payment_method='upi',
            upi_id=upi_id
        )
        
        # Update user payment status
        user.payment_status = 'completed'
        user.razorpay_payment_id = razorpay_payment_id
        user.razorpay_order_id = razorpay_order_id
        user.payment_amount = amount
        user.payment_date = timezone.now()
        user.save()
        
        return Response({
            'success': True,
            'transaction_id': transaction.id
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

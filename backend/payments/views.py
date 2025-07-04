from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Payment, Refund
from .serializers import PaymentSerializer, RefundSerializer
from orders.models import Order

class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
    
    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.request.data.get('order'), user=self.request.user)
        serializer.save(order=order)

class PaymentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_payment(request):
    """
    Process a payment for an order
    """
    order_id = request.data.get('order_id')
    payment_method = request.data.get('payment_method')
    amount = request.data.get('amount')
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=amount,
            status='pending'
        )
        
        # Here you would integrate with actual payment processor
        # For now, we'll simulate successful payment
        payment.status = 'completed'
        payment.save()
        
        # Update order status
        order.status = 'paid'
        order.save()
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class RefundListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Refund.objects.filter(payment__order__user=self.request.user)
    
    def perform_create(self, serializer):
        payment = get_object_or_404(
            Payment, 
            id=self.request.data.get('payment'), 
            order__user=self.request.user
        )
        serializer.save(payment=payment)

class RefundDetailAPIView(generics.RetrieveAPIView):
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Refund.objects.filter(payment__order__user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_refund(request):
    """
    Request a refund for a payment
    """
    payment_id = request.data.get('payment_id')
    refund_reason = request.data.get('reason', '')
    
    try:
        payment = Payment.objects.get(
            id=payment_id, 
            order__user=request.user,
            status='completed'
        )
        
        # Check if refund already exists
        if Refund.objects.filter(payment=payment).exists():
            return Response(
                {'error': 'Refund already requested for this payment'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create refund request
        refund = Refund.objects.create(
            payment=payment,
            amount=payment.amount,
            reason=refund_reason,
            status='pending'
        )
        
        serializer = RefundSerializer(refund)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found or not eligible for refund'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

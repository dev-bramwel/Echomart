from rest_framework import serializers
from django.db import models
from .models import Payment, Refund
from orders.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'amount', 'currency', 'payment_method',
            'transaction_id', 'status', 'gateway_response',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'order', 'transaction_id', 'gateway_response',
            'created_at', 'updated_at'
        ]


class CreatePaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = ['order_id', 'payment_method', 'currency']

    def validate_order_id(self, value):
        try:
            order = Order.objects.get(id=value, user=self.context['request'].user)
            if order.status != 'pending':
                raise serializers.ValidationError("Order is not in pending status")
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")

    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(id=order_id)
        validated_data['order'] = order
        validated_data['amount'] = order.total_amount
        return super().create(validated_data)


class RefundSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'payment', 'amount', 'reason', 'status',
            'refund_id', 'gateway_response',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'payment', 'refund_id', 'gateway_response',
            'created_at', 'updated_at'
        ]


class CreateRefundSerializer(serializers.ModelSerializer):
    payment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Refund
        fields = ['payment_id', 'amount', 'reason']

    def validate_payment_id(self, value):
        try:
            payment = Payment.objects.get(
                id=value, 
                order__user=self.context['request'].user,
                status='completed'
            )
            return value
        except Payment.DoesNotExist:
            raise serializers.ValidationError("Payment not found or not completed")

    def validate_amount(self, value):
        payment_id = self.initial_data.get('payment_id')
        if payment_id:
            try:
                payment = Payment.objects.get(id=payment_id)
                total_refunded = Refund.objects.filter(
                    payment=payment, 
                    status__in=['pending', 'completed']
                ).aggregate(total=models.Sum('amount'))['total'] or 0
                
                if total_refunded + value > payment.amount:
                    raise serializers.ValidationError(
                        "Refund amount exceeds available refundable amount"
                    )
            except Payment.DoesNotExist:
                pass
        return value

    def create(self, validated_data):
        payment_id = validated_data.pop('payment_id')
        payment = Payment.objects.get(id=payment_id)
        validated_data['payment'] = payment
        return super().create(validated_data)

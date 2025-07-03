from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal
import uuid
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod
from products.models import Product, ProductVariant
from .serializers import (
    CartSerializer, CartItemSerializer, AddToCartSerializer, 
    UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer,
    ShippingMethodSerializer
)

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=serializer.validated_data['product_id'])
    variant = None
    
    if serializer.validated_data.get('variant_id'):
        variant = ProductVariant.objects.get(id=serializer.validated_data['variant_id'])
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={'quantity': serializer.validated_data['quantity']}
    )
    
    if not created:
        cart_item.quantity += serializer.validated_data['quantity']
        cart_item.save()
    
    return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    serializer = UpdateCartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    quantity = serializer.validated_data['quantity']
    if quantity == 0:
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
    else:
        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return Response({'message': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)

class ShippingMethodListView(generics.ListAPIView):
    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    permission_classes = [permissions.AllowAny]

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    shipping_method = ShippingMethod.objects.get(
        id=serializer.validated_data['shipping_method_id']
    )
    
    with transaction.atomic():
        # Calculate totals
        subtotal = cart.total_price
        shipping_cost = shipping_method.cost
        tax_amount = subtotal * Decimal('0.1')  # 10% tax
        total_amount = subtotal + shipping_cost + tax_amount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_cost=shipping_cost,
            total_amount=total_amount,
            **{k: v for k, v in serializer.validated_data.items() 
               if k not in ['shipping_method_id', 'use_shipping_for_billing']}
        )
        
        # If using shipping address for billing
        if serializer.validated_data.get('use_shipping_for_billing', False):
            order.billing_first_name = order.shipping_first_name
            order.billing_last_name = order.shipping_last_name
            order.billing_email = order.shipping_email
            order.billing_phone = order.shipping_phone
            order.billing_address = order.shipping_address
            order.billing_city = order.shipping_city
            order.billing_country = order.shipping_country
            order.billing_postal_code = order.shipping_postal_code
            order.save()
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.subtotal
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

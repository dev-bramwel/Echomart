from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod
from products.serializers import ProductListSerializer, ProductVariantSerializer
from products.models import Product, ProductVariant

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    variant_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    subtotal = serializers.ReadOnlyField()
    unit_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'variant', 'product_id', 'variant_id', 
                 'quantity', 'unit_price', 'subtotal', 'created_at']
        read_only_fields = ['created_at']

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive")
        return value

    def validate_variant_id(self, value):
        if value:
            try:
                ProductVariant.objects.get(id=value)
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError("Product variant not found")
        return value

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive")
        return value

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description', 'cost', 'estimated_days']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'variant', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'subtotal', 'tax_amount', 
                 'shipping_cost', 'discount_amount', 'total_amount', 'items',
                 'shipping_first_name', 'shipping_last_name', 'shipping_email',
                 'shipping_phone', 'shipping_address', 'shipping_city', 
                 'shipping_country', 'shipping_postal_code', 'created_at', 
                 'updated_at', 'shipped_at', 'delivered_at']

class CreateOrderSerializer(serializers.Serializer):
    shipping_method_id = serializers.IntegerField()
    
    # Shipping Address
    shipping_first_name = serializers.CharField(max_length=50)
    shipping_last_name = serializers.CharField(max_length=50)
    shipping_email = serializers.EmailField()
    shipping_phone = serializers.CharField(max_length=15)
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField(max_length=100)
    shipping_country = serializers.CharField(max_length=100)
    shipping_postal_code = serializers.CharField(max_length=20)
    
    # Billing Address
    billing_first_name = serializers.CharField(max_length=50)
    billing_last_name = serializers.CharField(max_length=50)
    billing_email = serializers.EmailField()
    billing_phone = serializers.CharField(max_length=15)
    billing_address = serializers.CharField()
    billing_city = serializers.CharField(max_length=100)
    billing_country = serializers.CharField(max_length=100)
    billing_postal_code = serializers.CharField(max_length=20)
    
    use_shipping_for_billing = serializers.BooleanField(default=False)

    def validate_shipping_method_id(self, value):
        try:
            ShippingMethod.objects.get(id=value, is_active=True)
        except ShippingMethod.DoesNotExist:
            raise serializers.ValidationError("Shipping method not found or inactive")
        return value

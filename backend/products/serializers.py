from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, ProductReview, Wishlist

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'parent', 'subcategories', 'is_active']
    
    def get_subcategories(self, obj):
        subcategories = obj.subcategories.filter(is_active=True)
        return CategorySerializer(subcategories, many=True).data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'value', 'price_adjustment', 'stock_quantity', 'sku']

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'title', 'comment', 'is_verified_purchase', 'created_at']
        read_only_fields = ['user', 'is_verified_purchase', 'created_at']

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discounted_price', 'current_price', 'is_on_sale',
                 'stock_quantity', 'primary_image', 'category', 'featured', 'average_rating', 
                 'review_count', 'created_at']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        return None

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.count()

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'category', 'name', 'description', 'price', 'discounted_price',
                 'current_price', 'is_on_sale', 'stock_quantity', 'sku', 'weight', 'dimensions',
                 'is_digital', 'featured', 'tags', 'images', 'variants', 'reviews', 
                 'average_rating', 'review_count', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.count()

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'discounted_price', 
                 'stock_quantity', 'sku', 'weight', 'dimensions', 'is_digital', 
                 'featured', 'tags', 'is_active']

    def validate_sku(self, value):
        instance = getattr(self, 'instance', None)
        if instance and instance.sku == value:
            return value
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("SKU must be unique")
        return value

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['product'] = self.context['product']
        return super().create(validated_data)

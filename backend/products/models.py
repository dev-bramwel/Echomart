from django.db import models
from django.conf import settings
from vendors.models import Vendor
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)  # e.g., "10x20x30 cm"
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        return self.discounted_price if self.discounted_price else self.price

    @property
    def is_on_sale(self):
        return self.discounted_price is not None and self.discounted_price < self.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)  # e.g., "Size", "Color"
    value = models.CharField(max_length=100)  # e.g., "Large", "Red"
    price_adjustment = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.product.name} - {self.rating} stars by {self.user.email}"

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"

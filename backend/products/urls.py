from django.urls import path
from .views import (
    CategoryListAPIView,
    CategoryDetailAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    FeaturedProductsAPIView,
    search_products,
    ProductCreateAPIView,
    WishlistView,
    remove_from_wishlist,
    VendorProductListView,
    VendorProductDetailView
)

app_name = 'products'

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('featured/', FeaturedProductsAPIView.as_view(), name='featured-products'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('<int:product_id>/reviews/', ProductCreateAPIView.as_view(), name='product-reviews'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('<int:product_id>/wishlist/remove/', remove_from_wishlist, name='remove-from-wishlist'),
    path('search/', search_products, name='product-search'),
    
    # Vendor-only URLs
    path('vendor/products/', VendorProductListView.as_view(), name='vendor-product-list'),
    path('vendor/products/<int:pk>/', VendorProductDetailView.as_view(), name='vendor-product-detail'),
]

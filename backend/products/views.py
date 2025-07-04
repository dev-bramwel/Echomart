from rest_framework import generics, filters, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, ProductReview, Wishlist
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer, ProductReviewSerializer, ProductReviewCreateSerializer,
    WishlistSerializer
)

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None)

class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(is_active=True)

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'vendor', 'featured']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
            
        # In stock filtering
        in_stock = self.request.query_params.get('in_stock', None)
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
            
        return queryset

class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.filter(is_active=True)

class FeaturedProductsAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.filter(is_active=True, featured=True)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(tags__icontains=query),
            is_active=True
        )
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'query': query,
            'results': serializer.data,
            'count': products.count()
        })
    return Response({'query': '', 'results': [], 'count': 0})

class ProductCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductReview.objects.filter(product_id=product_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductReviewCreateSerializer
        return ProductReviewSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user, product=product)

class WishlistView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_wishlist(request, product_id):
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
        wishlist_item.delete()
        return Response({'message': 'Product removed from wishlist'}, status=status.HTTP_200_OK)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Product not in wishlist'}, status=status.HTTP_404_NOT_FOUND)

# Vendor-only views for product management
class VendorProductListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)

    def perform_create(self, serializer):
        # Ensure the user has a vendor profile
        if not hasattr(self.request.user, 'vendor_profile'):
            raise permissions.PermissionDenied("User must be a vendor to create products")
        serializer.save(vendor=self.request.user.vendor_profile)

class VendorProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductCreateUpdateSerializer

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)

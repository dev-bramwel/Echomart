from django.urls import path
from .views import (
    CartView,
    add_to_cart,
    update_cart_item,
    remove_cart_item,
    clear_cart,
    ShippingMethodListView,
    OrderListView,
    OrderDetailView,
    create_order
)

app_name = 'orders'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', add_to_cart, name='add-to-cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update-cart-item'),
    path('cart/remove/<int:item_id>/', remove_cart_item, name='remove-from-cart'),
    path('cart/clear/', clear_cart, name='clear-cart'),
    path('shipping-methods/', ShippingMethodListView.as_view(), name='shipping-methods'),
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', create_order, name='order-create'),
]

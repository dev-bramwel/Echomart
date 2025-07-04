from django.urls import path
from .views import (
    PaymentListCreateAPIView,
    PaymentDetailAPIView,
    process_payment,
    RefundListCreateAPIView,
    RefundDetailAPIView,
    request_refund
)

app_name = 'payments'

urlpatterns = [
    path('', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
    path('<int:pk>/', PaymentDetailAPIView.as_view(), name='payment-detail'),
    path('process/', process_payment, name='process-payment'),
    path('refunds/', RefundListCreateAPIView.as_view(), name='refund-list-create'),
    path('refunds/<int:pk>/', RefundDetailAPIView.as_view(), name='refund-detail'),
    path('refunds/request/', request_refund, name='request-refund'),
]

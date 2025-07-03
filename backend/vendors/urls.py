from django.urls import path
from .views import (
    VendorListAPIView,
    VendorDetailAPIView,
    VendorRegistrationAPIView,
    VendorProfileAPIView,
    VendorBankDetailsListAPIView,
    VendorBankDetailsAPIView,
    set_default_bank_account
)

app_name = 'vendors'

urlpatterns = [
    path('', VendorListAPIView.as_view(), name='vendor-list'),
    path('<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('register/', VendorRegistrationAPIView.as_view(), name='vendor-register'),
    path('profile/', VendorProfileAPIView.as_view(), name='vendor-profile'),
    path('bank-details/', VendorBankDetailsListAPIView.as_view(), name='vendor-bank-details-list'),
    path('bank-details/<int:pk>/', VendorBankDetailsAPIView.as_view(), name='vendor-bank-details-detail'),
    path('bank-details/<int:pk>/set-default/', set_default_bank_account, name='set-default-bank'),
]

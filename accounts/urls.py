from django.urls import path
from .views import VendorRegisterView, LoginView, vendor_dashboard, logout_view

urlpatterns = [
    path('register/', VendorRegisterView.as_view(), name='register'),   # POST /api/accounts/register/
    path('login/', LoginView.as_view(), name='login'),                  # POST /api/accounts/login/
    path('dashboard/', vendor_dashboard, name='dashboard'),             # GET  /api/accounts/dashboard/
    path('logout/', logout_view, name='logout'),                        # GET  /api/accounts/logout/
]

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token

# Home view
def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Home route
    path('api-auth/', include('rest_framework.urls')),  # Browsable API login
    path('api/token/', obtain_auth_token, name='api-token'),  # Token-based login
    path('api/accounts/', include('accounts.urls')),  # ✅ Your accounts app routes
    path('vendor/', include('vendors.urls')),  # ✅ FIXED: correct app name
]






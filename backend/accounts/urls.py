from django.urls import path
from .views import (
    UserRegistrationView,
    login_view,
    logout_view,
    UserProfileView,
    UserProfileUpdateView,
    change_password_view
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', login_view, name='user-login'),
    path('logout/', logout_view, name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('change-password/', change_password_view, name='change-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

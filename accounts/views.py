from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import VendorSerializer


# ✅ Vendor Registration API View (Supports GET + POST)
class VendorRegisterView(APIView):
    permission_classes = [AllowAny]

    # Optional GET method for browser visitors
    def get(self, request):  # type: ignore
        return Response({
            "message": "Welcome to the Vendor Registration API.",
            "usage": "Send a POST request with JSON data to register a new vendor.",
            "required_format": {
                "user": {
                    "username": "your_username",
                    "email": "your_email@example.com",
                    "password": "your_password"
                },
                "shop_name": "Your Shop Name",
                "phone": "Your Phone Number"
            }
        })

    # Handle registration POST
    def post(self, request):  # type: ignore
        serializer = VendorSerializer(data=request.data) # type: ignore
        if serializer.is_valid(): # type: ignore
            serializer.save() # type: ignore
            return Response({'message': 'Vendor registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # type: ignore


# ✅ Vendor Login API View (Token Authentication)
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):  # type: ignore
        serializer = self.serializer_class(data=request.data, context={'request': request}) # type: ignore
        serializer.is_valid(raise_exception=True) # type: ignore
        user = serializer.validated_data['user'] # type: ignore
        token, created = Token.objects.get_or_create(user=user) # type: ignore
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# ✅ Vendor Dashboard HTML View
@login_required
def vendor_dashboard(request):  # type: ignore
    return render(request, 'dashboard.html') # type: ignore


# ✅ Logout View (Session-based)
def logout_view(request):  # type: ignore
    logout(request) # type: ignore
    return redirect('home')  # 🔁 Ensure `home_view` is in your root urls.py

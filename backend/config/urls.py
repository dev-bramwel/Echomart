from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .views import ping

def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('ping/', ping, name='ping'),
]

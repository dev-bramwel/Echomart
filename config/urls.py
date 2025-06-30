from django.contrib import admin
from django.shortcuts import render
from django.urls import path

def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
]

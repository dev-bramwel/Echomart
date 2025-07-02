
from django.urls import path
from . import views

urlpatterns = [ # type: ignore
    path('register/', views.register_view, name='register'), # type: ignore
    path('dashboard/', views.vendor_dashboard, name='dashboard'), # type: ignore
]

from django.db import models
from django.contrib.auth.models import User

class AccountVendor(models.Model):  # ✅ Renamed to avoid conflict
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_vendor')
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name


from django.contrib import admin
from .models import AccountVendor  # ✅ Correct model name

@admin.register(AccountVendor)  # ✅ Register the correct model
class AccountVendorAdmin(admin.ModelAdmin): # type: ignore
    list_display = ['user', 'shop_name', 'phone', 'created_at']

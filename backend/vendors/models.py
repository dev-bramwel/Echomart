from django.db import models
from django.conf import settings

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=200)
    business_description = models.TextField()
    business_logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    business_address = models.TextField()
    business_phone = models.CharField(max_length=15)
    business_email = models.EmailField()
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

class VendorBankDetails(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=50, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.vendor.business_name} - {self.bank_name}"

    class Meta:
        unique_together = ['vendor', 'account_number']  # Prevent duplicate accounts

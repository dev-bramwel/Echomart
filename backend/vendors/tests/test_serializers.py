from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from vendors.models import Vendor, VendorBankDetails
from vendors.serializers import (
    VendorRegistrationSerializer,
    VendorSerializer,
    VendorBankDetailsSerializer,
    CreateBankDetailsSerializer,
    VendorUpdateSerializer,
)
from rest_framework.exceptions import ValidationError

User = get_user_model()

class VendorSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendoruser', password='pass123')
        self.factory = RequestFactory()

        self.vendor = Vendor.objects.create(
            user=self.user,
            business_name="Test Shop",
            business_description="We sell things",
            business_address="123 Nairobi Lane",
            business_phone="0712345678",
            business_email="test@shop.com",
            website="https://testshop.com"
        )

        def test_vendor_registration_serializer_valid(self):
        # Use a NEW user for this test, not self.user
            new_user = User.objects.create_user(username='newuser', password='pass456')

            data = {
                "business_name": "Fresh Market",
                "business_description": "Organic goods",
                "business_address": "789 New Street",
                "business_phone": "0711111111",
                "business_email": "fresh@market.com",
                "website": "https://freshmarket.com"
                }

            request = self.factory.post('/dummy-url/')
            request.user = new_user  # Important!

            serializer = VendorRegistrationSerializer(data=data, context={'request': request})
            self.assertTrue(serializer.is_valid(), serializer.errors)

            vendor = serializer.save()
            self.assertEqual(vendor.user, new_user)
            self.assertEqual(vendor.business_name, "Fresh Market")

    def test_vendor_update_serializer(self):
        data = {
            "business_name": "Updated Shop",
            "is_active": False
        }
        serializer = VendorUpdateSerializer(instance=self.vendor, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_vendor = serializer.save()
        self.assertEqual(updated_vendor.business_name, "Updated Shop")
        self.assertFalse(updated_vendor.is_active)

    def test_vendor_serializer_includes_bank_details(self):
        VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name="Bank A",
            account_name="Test Shop",
            account_number="111222333",
            routing_number="ROUTE001",
            is_default=True
        )
        serializer = VendorSerializer(self.vendor)
        self.assertIn('bank_details', serializer.data)
        self.assertEqual(len(serializer.data['bank_details']), 1)

    def test_bank_details_serializer_readonly_fields(self):
        bank = VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name="Bank A",
            account_name="Test Shop",
            account_number="111222333",
            routing_number="ROUTE001",
            is_default=False
        )
        serializer = VendorBankDetailsSerializer(bank)
        self.assertEqual(serializer.data['bank_name'], "Bank A")
        self.assertIn('created_at', serializer.data)
        self.assertTrue(serializer.fields['created_at'].read_only)

    def test_create_bank_details_unsets_previous_default(self):
        VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name="Old Bank",
            account_name="Test Shop",
            account_number="000111222",
            routing_number="OLD001",
            is_default=True
        )

        data = {
            "bank_name": "New Bank",
            "account_name": "Test Shop",
            "account_number": "333444555",
            "routing_number": "NEW002",
            "is_default": True
        }

        serializer = CreateBankDetailsSerializer(
            data=data, context={"vendor": self.vendor}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        new_bank = serializer.save()

        # Assert the new one is default, and old one is not
        self.assertTrue(new_bank.is_default)
        old_bank = VendorBankDetails.objects.get(account_number="000111222")
        self.assertFalse(old_bank.is_default)
    def test_vendor_registration_duplicate_rejected(self):
        data = {
        "business_name": "Another Shop",
        "business_description": "Dup shop",
        "business_address": "123 Somewhere",
        "business_phone": "0799999999",
        "business_email": "duplicate@shop.com",
        "website": "https://dupshop.com"
    }

        request = self.factory.post('/dummy-url/')
        request.user = self.user  # self.user already has a vendor from setUp()

        serializer = VendorRegistrationSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

def test_vendor_registration_invalid_missing_fields(self):
    new_user = User.objects.create_user(username='baduser', password='badpass')
    request = self.factory.post('/dummy-url/')
    request.user = new_user

    data = {
        "business_description": "Missing name",  # missing business_name
    }
    serializer = VendorRegistrationSerializer(data=data, context={'request': request})
    self.assertFalse(serializer.is_valid())
    self.assertIn('business_name', serializer.errors)

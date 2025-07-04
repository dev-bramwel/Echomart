from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from vendors.models import Vendor, VendorBankDetails
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class VendorAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testvendor', password='pass123')
        self.client = APIClient()

        # Use JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        self.vendor = Vendor.objects.create(
            user=self.user,
            business_name='Test Shop',
            business_description='Selling goods',
            business_address='123 Nairobi St',
            business_phone='0700123123',
            business_email='test@shop.com',
            is_verified=True
        )

        self.bank1 = VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name='Bank A',
            account_name='Test Shop',
            account_number='111222333',
            routing_number='ROUTE1',
            is_default=True
        )

    def test_vendor_list_public(self):
        url = reverse('vendors:vendor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('business_name', response.data['results'][0])

    def test_vendor_detail_public(self):
        url = reverse('vendors:vendor-detail', kwargs={'pk': self.vendor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['business_name'], 'Test Shop')

    def test_register_vendor_authenticated(self):
        url = reverse('vendors:vendor-register')
        response = self.client.post(url, {})  # Should fail since user already has a vendor
        self.assertEqual(response.status_code, 400)

    def test_vendor_profile_view(self):
        url = reverse('vendors:vendor-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['business_name'], 'Test Shop')

    def test_vendor_profile_update(self):
        url = reverse('vendors:vendor-profile')
        data = {'business_name': 'Updated Shop'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['business_name'], 'Updated Shop')

    def test_bank_details_list(self):
        url = reverse('vendors:vendor-bank-details-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_bank_details_create(self):
        url = reverse('vendors:vendor-bank-details-list')
        data = {
            'bank_name': 'Bank B',
            'account_name': 'Shop Account',
            'account_number': '222333444',
            'routing_number': 'ROUTE2'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['bank_name'], 'Bank B')

    def test_set_default_bank_account(self):
        # Add a second bank account (non-default)
        bank2 = VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name='Bank C',
            account_name='Test Shop',
            account_number='555666777',
            routing_number='ROUTE3',
            is_default=False
        )

        url = reverse('vendors:set-default-bank', kwargs={'pk': bank2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['bank_detail']['is_default'])

        # Check that the previous default was unset
        self.bank1.refresh_from_db()
        self.assertFalse(self.bank1.is_default)

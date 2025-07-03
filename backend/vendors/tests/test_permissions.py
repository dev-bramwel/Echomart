from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class VendorPermissionsTests(APITestCase):
    def test_unauthenticated_profile_access(self):
        response = self.client.get('/api/vendors/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_registration_access(self):
        response = self.client.post('/api/vendors/register/', {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_bank_detail_list(self):
        response = self.client.get('/api/vendors/bank-details/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    
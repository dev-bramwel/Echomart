from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class AccountsAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-register')
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('user-profile')

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "0712345678",
            "password": "strongpass123",
            "password_confirm": "strongpass123"
        }

    def test_user_can_register_successfully(self):
        
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from accounts.models import CustomUser
        self.assertTrue(CustomUser.objects.filter(email=self.user_data["email"]).exists())

    def test_user_registration_fails_with_mismatched_passwords(self):
        bad_data = self.user_data.copy()
        bad_data["password_confirm"] = "wrongpass"
        response = self.client.post(self.register_url, bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_returns_tokens(self):
        self.client.post(self.register_url, self.user_data)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_fails_with_wrong_credentials(self):
        self.client.post(self.register_url, self.user_data)
        bad_login_data = {
            "email": self.user_data["email"],
            "password": "wrongpass"
        }
        response = self.client.post(self.login_url, bad_login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_profile(self):
        self.client.post(self.register_url, self.user_data)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data["access"]

        # Send request with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_anonymous_user_cannot_view_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

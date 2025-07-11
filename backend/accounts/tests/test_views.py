from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.views import *



class UserRegistrationViewTest(APITestCase):
    def test_register_user(self):
        data = {
            "email": "register@example.com",
            "full_name": "New User",
            "phone_number": "0712345678",
            "password": "securepass123"
        }
        response = self.client.post(reverse("accounts:register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "register@example.com")


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="login@example.com",
            full_name="Login User",
            phone_number="0711222333",
            password="loginpass"
        )

    def test_valid_login(self):
        data = {"email": "login@example.com", "password": "loginpass"}
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login(self):
        data = {"email": "login@example.com", "password": "wrongpass"}
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="logout@example.com",
            full_name="Logout User",
            phone_number="0711000000",
            password="logoutpass"
        )
        login_response = self.client.post(reverse("accounts:login"), {
            "email": "logout@example.com",
            "password": "logoutpass"
        })
        self.token = login_response.data["refresh"]
        self.access = login_response.data["access"]

    def test_logout_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.post(reverse("accounts:logout"), {"refresh": self.token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged out")

    def test_logout_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        response = self.client.post(reverse("accounts:logout"), {"refresh": "invalid.token.here"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class UserProfileViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="profile@example.com",
            full_name="Profile User",
            phone_number="0711222333",
            password="profilepass"
        )
        login_response = self.client.post(reverse("accounts:login"), {
            "email": "profile@example.com",
            "password": "profilepass"
        })
        self.access = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_get_user_profile(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "profile@example.com")


class UserProfileUpdateViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="updateprofile@example.com",
            full_name="Update Profile",
            phone_number="0711999888",
            password="updateprofilepass"
        )
        UserProfile.objects.create(user=self.user)

        # 👇 Generate token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        login_response = self.client.post(reverse("accounts:login"), {
            "email": "updateprofile@example.com",
            "password": "updateprofilepass"
        })
        self.access = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_update_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "bio": "Updated Bio 2",
            "city": "Nairobi",
            "country": "Kenya"
        }
        response = self.client.patch(reverse("accounts:profile-update"), data, format="json")
        print("RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Updated Bio 2")


class ChangePasswordViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="changepass@example.com",
            full_name="Change Me",
            phone_number="0711444555",
            password="oldpassword"
        )
        login_response = self.client.post(reverse("accounts:login"), {
            "email": "changepass@example.com",
            "password": "oldpassword"
        })
        self.access = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_valid_password_change(self):
        data = {
            "old_password": "oldpassword",
            "new_password": "newsecure123",
            "confirm_password": "newsecure123"
        }
        response = self.client.post(reverse("accounts:change-password"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password changed successfully")

    def test_invalid_old_password(self):
        data = {
            "old_password": "wrongold",
            "new_password": "newsecure123",
            "confirm_password": "newsecure123"
        }
        response = self.client.post(reverse("accounts:change-password"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data)

    def test_mismatched_new_passwords(self):
        data = {
            "old_password": "oldpassword",
            "new_password": "newpass1",
            "confirm_password": "newpass2"
        }
        response = self.client.post(reverse("accounts:change-password"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

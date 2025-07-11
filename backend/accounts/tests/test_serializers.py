from django.test import TestCase, RequestFactory
from rest_framework.exceptions import ValidationError
from accounts.models import CustomUser, UserProfile
from accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    CustomUserUpdateSerializer,
    ChangePasswordSerializer
)


class UserRegistrationSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            "email": "newuser@example.com",
            "full_name": "New User",
            "phone_number": "0712345678",
            "password": "strongpass123"
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_missing_fields(self):
        data = {
            "email": "",
            "full_name": "",
            "phone_number": "",
            "password": ""
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("full_name", serializer.errors)
        self.assertIn("phone_number", serializer.errors)
        self.assertIn("password", serializer.errors)


class UserLoginSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="login@example.com",
            full_name="Login Test",
            phone_number="0700000000",
            password="loginpass"
        )
        self.factory = RequestFactory()

    def test_valid_login(self):
        data = {"email": "login@example.com", "password": "loginpass"}
        request = self.factory.post('/api/login/', data)
        serializer = UserLoginSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_invalid_login(self):
        data = {"email": "login@example.com", "password": "wrongpass"}
        request = self.factory.post('/api/login/', data)
        serializer = UserLoginSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("detail", serializer.errors)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="serialize@example.com",
            full_name="Serialized",
            phone_number="0700999999",
            password="serializepass"
        )

    def test_serialize_user(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data["email"], "serialize@example.com")
        self.assertIn("profile", serializer.data)


class CustomUserUpdateSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="update@example.com",
            full_name="Updatable User",
            phone_number="0700001111",
            password="updatepass"
        )

    def test_valid_update(self):
        data = {
            "username": "new_username",
            "full_name": "Updated Name",
            "phone_number": "0700002222",
            "date_of_birth": "1995-01-01"
        }
        serializer = CustomUserUpdateSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, "new_username")

    def test_duplicate_username(self):
        CustomUser.objects.create_user(
            email="taken@example.com",
            full_name="Taken User",
            phone_number="0711111111",
            password="pass123",
            username="takenuser"
        )
        self.user.username = "original"
        self.user.save()

        data = {"username": "takenuser"}
        serializer = CustomUserUpdateSerializer(instance=self.user, data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)


class ChangePasswordSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="changepass@example.com",
            full_name="Change Pass",
            phone_number="0712340000",
            password="oldpass123"
        )
        self.factory = RequestFactory()
        self.request = self.factory.post('/api/change-password/')
        self.request.user = self.user

    def test_passwords_match_and_old_password_valid(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "newpass456",
            "confirm_password": "newpass456"
        }
        serializer = ChangePasswordSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())

    def test_passwords_dont_match(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "newpass456",
            "confirm_password": "different"
        }
        serializer = ChangePasswordSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_wrong_old_password(self):
        data = {
            "old_password": "wrongpass",
            "new_password": "newpass456",
            "confirm_password": "newpass456"
        }
        serializer = ChangePasswordSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

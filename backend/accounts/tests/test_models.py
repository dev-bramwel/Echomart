from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, UserProfile


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            full_name='Test User',
            phone_number='0712345678',
            password='securepassword123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertTrue(self.user.check_password('securepassword123'))
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_superuser_creation(self):
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            phone_number='0799999999',
            password='adminpass'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_missing_email_raises_error(self):
        with self.assertRaisesMessage(ValueError, "Email is required"):
            CustomUser.objects.create_user(
                email='',
                full_name='Missing Email',
                phone_number='0700000000',
                password='pass'
            )

    def test_missing_full_name_raises_error(self):
        with self.assertRaisesMessage(ValueError, "Full name is required"):
            CustomUser.objects.create_user(
                email='nofull@example.com',
                full_name='',
                phone_number='0700000000',
                password='pass'
            )

    def test_missing_phone_number_raises_error(self):
        with self.assertRaisesMessage(ValueError, "Phone number is required"):
            CustomUser.objects.create_user(
                email='nophone@example.com',
                full_name='No Phone',
                phone_number='',
                password='pass'
            )

    def test_full_name_normalization(self):
        messy_name = "  John   Doe   "
        user = CustomUser.objects.create_user(
            email="cleanname@example.com",
            full_name=messy_name,
            phone_number="0700123456",
            password="testpass"
        )
        self.assertEqual(user.full_name, "John Doe")


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='profileuser@example.com',
            full_name='Profile User',
            phone_number='0701234567',
            password='pass123'
        )
        UserProfile.objects.filter(user=self.user).delete()
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='I am a test user',
            address='Test Street',
            city='Testville',
            country='Testland',
            postal_code='00100'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.email, 'profileuser@example.com')
        self.assertEqual(str(self.profile), "profileuser@example.com's Profile")
        self.assertEqual(self.profile.bio, 'I am a test user')

from django.test import TestCase
from accounts.models import CustomUser, UserProfile


class UserSignalTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="signaltest@example.com",
            full_name="Signal Tester",
            phone_number="0712345678",
            password="testpass"
        )

    def test_profile_created_on_user_creation(self):
        """Check that a profile is automatically created when a user is registered."""
        profile = UserProfile.objects.filter(user=self.user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)

    def test_profile_saved_on_user_update(self):
        """Ensure profile is still intact and updated when user is updated."""
        old_updated_at = self.user.profile.updated_at if hasattr(self.user.profile, "updated_at") else None
        self.user.full_name = "Updated Name"
        self.user.save()
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user.full_name, "Updated Name")  # Ensure profile still linked correctly

    def test_signal_does_not_duplicate_profiles(self):
        """Ensure that updating a user does not create a duplicate profile."""
        self.user.full_name = "No Duplicate"
        self.user.save()
        profiles = UserProfile.objects.filter(user=self.user)
        self.assertEqual(profiles.count(), 1)

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import force_authenticate, APIRequestFactory

from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class SimpleJWTTokenTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="jwtuser@example.com",
            full_name="JWT User",
            phone_number="0712345678",
            password="jwtpass123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token

    def test_generate_and_validate_access_token(self):
        # Validate token manually
        token = AccessToken(str(self.access))
        self.assertEqual(token['user_id'], self.user.id)

    def test_refresh_token_returns_new_access(self):
        # Simulate refreshing
        new_access = self.refresh.access_token
        self.assertNotEqual(str(new_access), str(self.access))

    def test_token_expiry_manually(self):
        # Simulate expired token
        token = AccessToken.for_user(self.user)
        token.set_exp(from_time=timezone.now() - timedelta(hours=1))  # expired 1hr ago

        with self.assertRaises(TokenError):
            AccessToken(str(token)).check_exp()


class JWTAuthenticationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="authtest@example.com",
            full_name="Auth Tester",
            phone_number="0700111222",
            password="authpass"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)
        self.factory = APIRequestFactory()
        self.auth = JWTAuthentication()

    def test_valid_token_authenticates_user(self):
        request = self.factory.get("/secure-endpoint/")
        request.META['HTTP_AUTHORIZATION'] = f"Bearer {self.access}"
        user_auth_tuple = self.auth.authenticate(request)
        self.assertIsNotNone(user_auth_tuple)
        user, _ = user_auth_tuple
        self.assertEqual(user.email, self.user.email)

    def test_missing_token_returns_none(self):
        request = self.factory.get("/secure-endpoint/")
        self.assertIsNone(self.auth.authenticate(request))

    def test_invalid_token_raises_auth_error(self):
        request = self.factory.get("/secure-endpoint/")
        request.META['HTTP_AUTHORIZATION'] = "Bearer invalid.token.string"
        with self.assertRaises(AuthenticationFailed):
            self.auth.authenticate(request)


class PermissionEnforcementTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="permuser@example.com",
            full_name="Permission User",
            phone_number="0799999999",
            password="perm123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)
        self.factory = APIRequestFactory()

    def test_is_authenticated_blocks_unauthenticated(self):
        class SecureView(APIView):
            permission_classes = [IsAuthenticated]
            def get(self, request): return Response({"ok": True})

        view = SecureView.as_view()
        request = self.factory.get("/secure-endpoint/")
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_is_authenticated_allows_authenticated(self):
        class SecureView(APIView):
            permission_classes = [IsAuthenticated]
            def get(self, request): return Response({"ok": True})

        request = self.factory.get("/secure-endpoint/")
        request.META['HTTP_AUTHORIZATION'] = f"Bearer {self.access}"
        view = SecureView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"ok": True})

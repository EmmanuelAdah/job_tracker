import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a user with email instead of username."""
        email = 'dev@example.com'
        user = User.objects.create_user(
            email=email,
            password='password123',
            first_name='Gemini',
            last_name='User'
        )
        self.assertEqual(user.email, email)
        self.assertIsInstance(user.id, uuid.UUID)
        self.assertTrue(user.is_active)

    def test_new_user_invalid_email(self):
        """Test that missing email raises a ValueError."""
        with self.assertRaisesMessage(ValueError, 'The Email field must be occupied'):
            User.objects.create_user(email=None, password='password123')

    def test_name_validators(self):
        """Test RegexValidator only allows letters in names."""
        user = User(email="test@test.com", first_name="John123", last_name="Doe")
        # full_clean() triggers the validators defined on the model fields
        with self.assertRaises(ValidationError):
            user.full_clean()



User = get_user_model()

class UserApiTests(APITestCase):

    def setUp(self):
        # Based on your URLs: /user/register/, /user/login/, /user/profile/
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.profile_url = reverse('user_profile')

        self.user_data = {
            "email": "tester@example.com",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration_api(self):
        """Test POST to /user/register/"""
        payload = {
            "email": "new@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['email'], "new@example.com")

    def test_user_login_api(self):
        """Test POST to /user/login/ returns JWT tokens."""
        payload = {
            "email": "tester@example.com",
            "password": "securepassword123"
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_user_profile_authenticated(self):
        """Test GET /user/profile/ with JWT authentication."""
        # This simulates a valid JWT header
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_profile_patch(self):
        """Test PATCH /user/profile/ partial update."""
        self.client.force_authenticate(user=self.user)
        payload = {"first_name": "UpdatedName"}
        response = self.client.patch(self.profile_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedName")

    def test_delete_profile(self):
        """Test DELETE /user/profile/ removes the user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_profile_unauthorized(self):
        """Test that profile access is blocked without authentication."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

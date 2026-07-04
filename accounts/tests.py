from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class AuthTests(APITestCase):
    def test_register_success(self):
        resp = self.client.post('/api/auth/register/', {
            'name': 'Alice', 'email': 'alice@test.com', 'password': 'testpass123'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], 'Alice')
        self.assertEqual(resp.data['email'], 'alice@test.com')
        self.assertNotIn('password', resp.data)

    def test_register_duplicate_email(self):
        User.objects.create_user(email='dup@test.com', name='First', password='testpass123')
        resp = self.client.post('/api/auth/register/', {
            'name': 'Second', 'email': 'dup@test.com', 'password': 'testpass123'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', resp.data)

    def test_register_short_password(self):
        resp = self.client.post('/api/auth/register/', {
            'name': 'Bob', 'email': 'bob@test.com', 'password': 'short'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(email='login@test.com', name='Login', password='testpass123')
        resp = self.client.post('/api/auth/login/', {
            'email': 'login@test.com', 'password': 'testpass123'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)

    def test_login_invalid_credentials(self):
        resp = self.client.post('/api/auth/login/', {
            'email': 'nobody@test.com', 'password': 'wrong'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        user = User.objects.create_user(email='refresh@test.com', name='Refresh', password='testpass123')
        refresh = RefreshToken.for_user(user)
        resp = self.client.post('/api/auth/token/refresh/', {
            'refresh': str(refresh)
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)

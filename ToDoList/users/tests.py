from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from django.urls import reverse

loginURL = reverse('login')
registerURL = reverse('register')

# Create your tests here.
class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_valid(self):
        data = {
            'first_name': 'Test1',
            'username': 'testuser1',
            'password': 'testpassword'
        }
        good_response = self.client.post(registerURL, data)
        self.assertEqual(good_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)
    
    def test_register_user_invalid_password(self):
        data = {
            'first_name': 'Test2',
            'username': 'testuser2',
            'password': 'pwd2'
        }
        bad_response = self.client.post(registerURL, data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)
    
    def test_register_user_invalid_username(self):
        data = {
            'first_name': 'Test3',
            'username': 'testuser3',
            'password': 'testpassword'
        }
        # Create a user with the username
        User(first_name='AnotherFirstName', username=data['username'], password='anotherpassword').save()

        # Attempt to register again with the same username
        bad_response = self.client.post(registerURL, data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)
    
    def test_register_user_missing_fields(self):
        data = {
            'first_name': 'Test4',
            'username': 'testuser4'
            # Missing password
        }
        bad_response = self.client.post(registerURL, data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)
    
    def test_register_user_empty_fields(self):
        data = {
            'first_name': '',
            'username': '',
            'password': ''
        }
        bad_response = self.client.post(registerURL, data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)

class UserLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User(first_name='TestUser', username='testuser', password='testpassword').save()

    def test_login_user_valid(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(loginURL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_invalid_password(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(loginURL, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user_nonexistent(self):
        data = {
            'username': 'nonexistentuser',
            'password': 'somepassword'
        }
        response = self.client.post(loginURL, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_login_user_missing_fields(self):
        data = {
            'username': 'testuser'
            # Missing password
        }
        response = self.client.post(loginURL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_user_empty_fields(self):
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(loginURL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserRefreshTokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User(first_name='TestUser', username='testuser', password='testpassword').save()
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(loginURL, login_data)
        self.refresh_token = response.data['refresh']

    def test_refresh_token_valid(self):
        data = {
            'refresh': self.refresh_token
        }
        response = self.client.post(reverse('refresh_token'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_invalid(self):
        data = {
            'refresh': 'invalidtoken'
        }
        response = self.client.post(reverse('refresh_token'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_missing(self):
        data = {}
        response = self.client.post(reverse('refresh_token'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
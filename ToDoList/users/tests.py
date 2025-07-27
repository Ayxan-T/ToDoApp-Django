from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from django.urls import reverse

# Create your tests here.
class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Test user registration
    def test_register_user_valid(self):
        data = {
            'first_name': 'Test1',
            'username': 'testuser1',
            'password': 'testpassword'
        }
        good_response = self.client.post(reverse('register'), data)
        self.assertEqual(good_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)
    def test_register_user_invalid_password(self):
        data = {
            'first_name': 'Test2',
            'username': 'testuser2',
            'password': 'pwd2'
        }
        bad_response = self.client.post(reverse('register'), data)
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
        bad_response = self.client.post(reverse('register'), data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)
    def test_register_user_missing_fields(self):
        data = {
            'first_name': 'Test4',
            'username': 'testuser4'
            # Missing password
        }
        bad_response = self.client.post(reverse('register'), data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)
    def test_register_user_empty_fields(self):
        data = {
            'first_name': '',
            'username': '',
            'password': ''
        }
        bad_response = self.client.post(reverse('register'), data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)
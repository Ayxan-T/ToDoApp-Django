from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

# Create your tests here.
class UserTests(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        self.client = APIClient()

    def test_register_user_valid(self):
        # Test user creation logic
        data = {
            'first_name': 'Test1',
            'username': 'testuser1',
            'password': 'testpassword'
        }
        good_response = self.client.post('/users/register/', data)
        self.assertEqual(good_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)
    
    def test_register_user_invalid_password(self):
        data = {
            'first_name': 'Test2',
            'username': 'testuser2',
            'password': 'pwd2'
        }
        bad_response = self.client.post('/users/register/', data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)
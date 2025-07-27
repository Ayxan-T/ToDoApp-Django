from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from tasks.models import Task
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
userTasksURL = reverse('get_user_tasks')
class UserTasksTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User(first_name='TestUser', username='testuser', password='testpassword')
        self.user.save()

        self.refresh = RefreshToken()
        self.refresh['user_id'] = self.user.id
        self.refresh['username'] = self.user.username

        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.access_token}')

    def create_tasks(self, user):
        for i in range(15):
            Task(
                title=f'Task {i}',
                description=f'Description for task {i}',
                user_id = self.user
            ).save()

    def test_get_user_tasks(self):
        # Test without tasks
        response = self.client.get(userTasksURL) # Get default page = 1 -> exceeds total_pages (0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Page number exceeds total pages')

        # Test with tasks: first page
        self.create_tasks(self.user) # Create 15 tasks for the user
        response = self.client.get(userTasksURL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['current_page'], 1)
        self.assertEqual(response.data['total_pages'], 2)

        # Test with tasks: second page
        response = self.client.get(userTasksURL + '?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['current_page'], 2)
    
    def test_get_user_tasks_invalid_page(self):
        response = self.client.get(userTasksURL + '?page=invalid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_user_tasks_page_exceeds_total(self):
        response = self.client.get(userTasksURL + '?page=9999')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

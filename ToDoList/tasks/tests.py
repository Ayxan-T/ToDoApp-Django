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

    def create_tasks(self):
        Status = ['new', 'in_progress', 'completed']
        for i in range(15):
            Task(
                title=f'Task {i}',
                description=f'Description for task {i}',
                status=Status[i % 3],
                user_id = self.user
            ).save()

    def test_get_user_tasks(self):
        # Test without tasks
        response = self.client.get(userTasksURL) # Get default page = 1
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

        # Test with tasks: first page
        self.create_tasks() # Create 15 tasks for the user
        response = self.client.get(userTasksURL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

        # Test with tasks: second page
        response = self.client.get(userTasksURL + '?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
    
    def test_get_user_tasks_invalid_page(self):
        response = self.client.get(userTasksURL + '?page=invalid')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_user_tasks_page_exceeds_total(self):
        response = self.client.get(userTasksURL + '?page=9999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_tasks_with_status_filter(self):
        self.create_tasks()
        response = self.client.get(userTasksURL + '?status=new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # 5 tasks with status 'new'
        for task in response.data['results']:
            self.assertEqual(task['status'], 'new')
        
        # Test with invalid status
        response = self.client.get(userTasksURL + '?status=invalid_status')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid status')

        

class TaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User(first_name='TestUser', username='testuser', password='testpassword')
        self.user.save()

        self.refresh = RefreshToken()
        self.refresh['user_id'] = self.user.id
        self.refresh['username'] = self.user.username

        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'Task description'
        }
        response = self.client.post(reverse('create_task'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_get_task_by_id(self):
        task = Task(title='Test Task', description='Test Description', user_id=self.user)
        task.save()
        good_response = self.client.get(reverse('get_task_by_id', args=[task.id]))
        self.assertEqual(good_response.status_code, status.HTTP_200_OK)
        bad_response = self.client.get(reverse('get_task_by_id', args=[9999]))  # Non-existent task
        self.assertEqual(bad_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_task(self):
        task = Task(title='Old Title', description='Old Description', user_id=self.user)
        task.save()
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'status': 'in_progress'
        }
        response = self.client.patch(reverse('update_task', args=[task.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_task_not_found(self):
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        response = self.client.patch(reverse('update_task', args=[9999]), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_task(self):
        task = Task(title='Task to Delete', description='Delete this task', user_id=self.user)
        task.save()
        response = self.client.delete(reverse('delete_task', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_task_not_found(self):
        response = self.client.delete(reverse('delete_task', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_completed(self):
        task = Task(title='Task to Complete', description='Complete this task', user_id=self.user)
        task.save()
        response = self.client.patch(reverse('task_completed', args=[task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=task.id)
        self.assertEqual(task.status, 'completed')
    
    def test_task_completed_not_found(self):
        response = self.client.patch(reverse('task_completed', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
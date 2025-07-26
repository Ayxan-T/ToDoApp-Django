from rest_framework.response import Response
from rest_framework.decorators import api_view

from .decorators import check_authorization
from .models import Task
from users.models import User
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

# Create your views here.
'''
@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
'''

@api_view(['GET'])
@check_authorization
def get_user_tasks(request):
    tasks = Task.objects.filter(user_id=request.user_id)
    serialized_tasks = TaskSerializer(tasks, many=True)
    return Response(serialized_tasks.data)

@api_view(['GET'])
@check_authorization
def get_task_by_id(request, task_id):    
    try:
        task = Task.objects.get(id=task_id, user_id=request.user_id)
        serialized_task = TaskSerializer(task)
        return Response(serialized_task.data)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@check_authorization
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        user_instance = User.objects.get(id=request.user_id)
        serializer.save(user_id=user_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
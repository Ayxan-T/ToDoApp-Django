from rest_framework.response import Response
from rest_framework.decorators import api_view

from .decorators import check_authorization
from .models import Task
from users.models import User
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class TaskPagination(PageNumberPagination):
    page_size = 10  # Number of tasks per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum number of tasks per page

@api_view(['GET'])
@check_authorization
def get_user_tasks(request):
    user_id = request.user_id
    Status = request.query_params.get('status', None)
    if Status:
        valid_statuses = {'new', 'in_progress', 'completed'}
        if Status not in valid_statuses:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        tasks = Task.objects.filter(user_id=user_id, status=Status).order_by('id')
    else:
        # If no status filter is applied, get all tasks for the user
        tasks = Task.objects.filter(user_id=user_id).order_by('id')
    
    paginator = TaskPagination()
    paginated_tasks = paginator.paginate_queryset(tasks, request)
    
    serializer = TaskSerializer(paginated_tasks, many=True)
    return paginator.get_paginated_response(serializer.data)

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

@api_view(['PATCH'])
@check_authorization
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user_id=request.user_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
@check_authorization
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user_id=request.user_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PATCH'])
@check_authorization
def task_completed(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user_id=request.user_id)
        task.status = 'completed'
        task.save()
        return Response({'message': 'Task marked as completed'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
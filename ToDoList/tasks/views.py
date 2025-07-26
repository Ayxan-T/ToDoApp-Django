from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from users.models import User
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

# Create your views here.
@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_tasks(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'error': 'Authorization tokens are missing.'}, status=status.HTTP_401_UNAUTHORIZED)
    token = auth_header.split(' ')[1]
    try:
        token = AccessToken(token)
        user = token['user_id']
        if not User.objects.filter(id=user).exists():
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    tasks = Task.objects.filter(user_id=user)
    serialized_tasks = TaskSerializer(tasks, many=True)
    return Response(serialized_tasks.data)
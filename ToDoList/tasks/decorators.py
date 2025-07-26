from functools import wraps
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from users.models import User
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

def check_authorization(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authorization tokens are missing.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        try:
            token = AccessToken(token)
            user_id = token['user_id']
            if not User.objects.filter(id=user_id).exists():
                return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
            request.user_id = user_id
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        return f(request, *args, **kwargs)
    return wrapper
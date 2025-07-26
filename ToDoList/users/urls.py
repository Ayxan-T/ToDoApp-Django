from django.urls import path
from .views import register_user, login_user, refresh_token


urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('refresh-token/', refresh_token)
]

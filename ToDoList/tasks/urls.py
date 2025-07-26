from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_tasks),
    path("user-tasks/", views.get_user_tasks),
]
from django.urls import path
from . import views

urlpatterns = [
    path("user-tasks/", views.get_user_tasks, name='get_user_tasks'),
    path("<int:task_id>/", views.get_task_by_id, name='get_task_by_id'),
    path("create-task/", views.create_task, name='create_task'),
    path("update-task/<int:task_id>/", views.update_task, name='update_task'),
    path("delete-task/<int:task_id>/", views.delete_task, name='delete_task'),

    path("mark-completed/<int:task_id>/", views.task_completed, name='task_completed'),
]
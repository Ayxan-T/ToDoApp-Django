from django.urls import path
from . import views

urlpatterns = [
    path("user-tasks/", views.get_user_tasks, name='get_user_tasks'),
    path("task/<int:task_id>/", views.get_task_by_id, name='get_task_by_id'),
    path("create-task/", views.create_task, name='create_task'),
    path("update-task/<int:task_id>/", views.update_task, name='update_task'),
    path("delete-task/<int:task_id>/", views.delete_task, name='delete_task'),

    path("task/<int:task_id>/completed/", views.task_completed, name='task_completed'),
    path("filter-by-status/<str:status>/", views.filter_tasks_by_status, name='filter_tasks_by_status'),

    # Uncomment the following line to enable the endpoint for getting all tasks
    # path("", views.get_all_tasks)
]
from django.urls import path
from . import views

urlpatterns = [
    path("user-tasks/", views.get_user_tasks),
    path("task/<int:task_id>/", views.get_task_by_id),
    path("create-task/", views.create_task),

    # Uncomment the following line to enable the endpoint for getting all tasks
    # path("", views.get_all_tasks)
]
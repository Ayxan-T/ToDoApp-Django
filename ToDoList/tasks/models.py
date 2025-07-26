from django.db import models
from users.models import User

# Create your models here.
class Task(models.Model):
    status_of_task = [
        ('new','New'),
        ('in_progress', 'In Progress'),
        ('completed','Completed')
    ]
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices= status_of_task, default='new')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"{self.id}: {self.title} ({self.status})"
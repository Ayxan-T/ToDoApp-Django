from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(validators=[MinLengthValidator(6)])

    def __str__(self):
        return f"{self.username}"
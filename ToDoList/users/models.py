from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=120, validators=[MinLengthValidator(6)])

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username}"
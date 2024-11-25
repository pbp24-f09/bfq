from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.URLField(max_length=200, blank=True, null=True)

    # Assign the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

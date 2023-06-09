from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    bio = models.CharField(max_length=150, blank=True, null=True)

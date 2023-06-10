from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=150)

    REQUIRED_FIELDS = []
    objects = UserManager()
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_set'  # Add a custom related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set'  # Add a custom related_name
    )

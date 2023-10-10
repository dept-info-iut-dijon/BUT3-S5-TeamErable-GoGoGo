from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(max_length=5000, null=True)
    friends = models.ManyToManyField('self', blank=True)
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_set',  # You can choose a related_name of your choice
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set',  # You can choose a related_name of your choice
        related_query_name='customuser'
    )


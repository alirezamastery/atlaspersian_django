import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from users.managers import UserManager


__all__ = [
    'User'
]


class User(AbstractBaseUser, PermissionsMixin):
    username = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mobile = models.CharField(max_length=15, unique=True, blank=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.mobile)

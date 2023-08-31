import uuid

from django.db import models


__all__ = [
    'Address'
]


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='addresses')

    title = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    details = models.TextField()

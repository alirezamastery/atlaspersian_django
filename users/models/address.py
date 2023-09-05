import uuid

from django.db import models


__all__ = [
    'Address',
    'Province',
    'City',
]


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    title = models.CharField(max_length=255, default='', blank=True)
    postal_code = models.CharField(max_length=255)
    province = models.ForeignKey(
        'users.Province',
        on_delete=models.PROTECT,
        related_name='user_addresses'
    )
    city = models.ForeignKey(
        'users.City',
        on_delete=models.PROTECT,
        related_name='user_addresses'
    )
    details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Province(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'


class City(models.Model):
    title = models.CharField(max_length=255)
    province = models.ForeignKey(
        'users.Province',
        on_delete=models.CASCADE,
        related_name='cities'
    )

    def __str__(self):
        return f'{self.title}'

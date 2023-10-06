from django.db import models


__all__ = [
    'ShippingMethod',
]


class ShippingMethod(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=True)
    cost = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.title}'

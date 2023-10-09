import uuid

from django.db import models


__all__ = [
    'PaymentMethod',
    'Payment',
]


class PaymentMethod(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=True)
    is_taxable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Payment(models.Model):
    class Status(models.TextChoices):
        REJECTED = 'REJECTED'
        INVALID = 'INVALID'
        VERIFIED = 'VERIFIED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_id = models.CharField(max_length=255, unique=True)
    method = models.ForeignKey('shop.PaymentMethod', on_delete=models.PROTECT, related_name='payments')
    order = models.ForeignKey('shop.Order', on_delete=models.PROTECT, related_name='payments')
    card_digits = models.CharField(max_length=255, blank=True, null=True)
    amount = models.PositiveBigIntegerField()
    date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

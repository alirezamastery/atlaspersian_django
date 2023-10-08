import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from shop.models import PriceModel


__all__ = [
    'Order',
    'OrderItem',
]


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING_PAYMENT = 'PENDING_PAYMENT'
        CANCELED_USER = 'CANCELED_USER'
        CANCELED_ADMIN = 'CANCELED_ADMIN'
        PAID = 'PAID'
        SENT = 'SENT'
        DELIVERED = 'DELIVERED'
        COMPLETED = 'COMPLETED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveBigIntegerField(default=109010, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='shop_orders')
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING_PAYMENT)
    pay_method = models.ForeignKey('shop.PaymentMethod', on_delete=models.PROTECT, related_name='orders')
    ship_method = models.ForeignKey('shop.ShippingMethod', on_delete=models.PROTECT, related_name='orders')
    address = models.ForeignKey('users.Address', on_delete=models.PROTECT, related_name='orders')
    user_note = models.TextField(default='', blank=True)

    is_verified = models.BooleanField(default=False)

    pay_amount = models.PositiveBigIntegerField()
    shipping_cost = models.PositiveBigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.number} - {self.created_at}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_number = Order.objects.all().aggregate(largest=models.Max('number'))['largest']
            if last_number is not None:
                self.number = last_number + 1
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        pass


class OrderItem(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.PROTECT, related_name='items')
    variant = models.ForeignKey('shop.Variant', on_delete=models.PROTECT, related_name='order_items')

    quantity = models.PositiveIntegerField()
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(99)])

    raw_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])
    selling_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'variant'],
                name='unique_order_variant'
            )
        ]

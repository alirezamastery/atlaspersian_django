from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


__all__ = [
    'Variant',
    'SelectorType',
    'SelectorValue',
]


class Variant(models.Model):
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='variants'
    )
    selector_value = models.ForeignKey(
        'shop.SelectorValue',
        on_delete=models.PROTECT,
        related_name='product_variants'
    )

    is_active = models.BooleanField(default=True)
    inventory = models.PositiveIntegerField()
    max_in_order = models.PositiveIntegerField(default=5)

    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(99)])
    discount_value = models.PositiveBigIntegerField(default=0)

    raw_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])
    selling_price = models.PositiveBigIntegerField(validators=[MinValueValidator(10000)])

    sale_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'selector_value'],
                name='unique_product_selector_value'
            )
        ]

    def __str__(self):
        return f'{self.product} - {self.selector_value.value}'

    def save(self, **kwargs):
        decimal = settings.PRICE_DECIMAL

        self.raw_price = round(self.raw_price, decimal)
        self.discount_value = round(self.raw_price * self.discount_percent / 100, decimal)
        selling_price = self.raw_price * (100 - self.discount_percent) / 100
        self.selling_price = round(selling_price, decimal)

        super().save(**kwargs)

    def delete(self, using=None, keep_parents=False):
        pass


class SelectorType(models.Model):
    class CodeChoices(models.TextChoices):
        SIZE = 'SIZE'
        COLOR = 'COLOR'

    title = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True, choices=CodeChoices.choices)

    def __str__(self):
        return f'{self.title}'


class SelectorValue(models.Model):
    type = models.ForeignKey(
        'shop.SelectorType',
        on_delete=models.PROTECT,
        related_name='values'
    )
    title = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255, unique=True)
    extra_info = models.TextField(default='')

    def __str__(self):
        return f'{self.type} - {self.value}'

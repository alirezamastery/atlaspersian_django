from django.db import models


__all__ = [
    'Attribute',
    'AttributeUnit',
]


class Attribute(models.Model):
    class Types(models.TextChoices):
        NUMBER = 'NUMBER'
        SHORT_TEXT = 'SHORT_TEXT'
        LONG_TEXT = 'LONG_TEXT'
        BOOLEAN = 'BOOLEAN'

    title = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255, choices=Types.choices, default=Types.NUMBER, blank=True)
    description = models.TextField(default='', blank=True)

    unit = models.ForeignKey(
        'shop.AttributeUnit',
        on_delete=models.PROTECT,
        related_name='attributes',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class AttributeUnit(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

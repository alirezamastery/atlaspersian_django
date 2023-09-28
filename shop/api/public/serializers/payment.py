from rest_framework import serializers

from shop.models import *


__all__ = [
    'PaymentMethodReadSerializerPublic',
]


class PaymentMethodReadSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id',
            'type',
            'title',
            'description',
            'is_active',
            'is_taxable',
        ]

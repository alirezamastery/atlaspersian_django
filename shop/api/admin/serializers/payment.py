from rest_framework.serializers import ModelSerializer

from shop.models import *


__all__ = [
    'PaymentMethodReadSerializer',
    'PaymentMethodWriteSerializer',
]


class PaymentMethodReadSerializer(ModelSerializer):
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


class PaymentMethodWriteSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'type',
            'title',
            'description',
            'is_active',
            'is_taxable',
        ]

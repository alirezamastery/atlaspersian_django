from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import *


__all__ = [
    'PaymentMethodReadSerializerPublic',
]


class PaymentMethodReadSerializerPublic(ModelSerializer):
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

from rest_framework.serializers import ModelSerializer

from shop.models import *


__all__ = [
    'ShippingMethodReadSerializer',
    'ShippingMethodWriteSerializer',
]


class ShippingMethodReadSerializer(ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [
            'id',
            'type',
            'title',
            'description',
            'is_active',
            'cost',
        ]


class ShippingMethodWriteSerializer(ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [
            'type',
            'title',
            'description',
            'is_active',
            'cost',
        ]

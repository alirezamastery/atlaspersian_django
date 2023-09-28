from rest_framework import serializers

from shop.models import *


__all__ = [
    'ShippingMethodReadSerializerPublic',
]


class ShippingMethodReadSerializerPublic(serializers.ModelSerializer):
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

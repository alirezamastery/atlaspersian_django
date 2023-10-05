from rest_framework import serializers

from shop.models import *


__all__ = [
    '_OrderItemReadSerializer',
]


class _Variant(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'product_id',
            'selector_value_id',
            'is_active'
        ]


class _OrderItemReadSerializer(serializers.ModelSerializer):
    variant = _Variant(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'variant',
            'selling_price',
            'quantity'
        ]

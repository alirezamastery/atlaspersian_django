from rest_framework import serializers

from shop.models import *
from ._sub import (
    _ProductSerializer,
    _VariantSelectorValueReadSerializer
)


__all__ = [
    'VariantReadSerializerAdmin',
]


class VariantReadSerializerAdmin(serializers.ModelSerializer):
    product = _ProductSerializer(read_only=True)
    selector_value = _VariantSelectorValueReadSerializer(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'is_active',
            'inventory',
            'max_in_order',
            'discount_percent',
            'raw_price',
            'selling_price',
            'sale_count',
        ]

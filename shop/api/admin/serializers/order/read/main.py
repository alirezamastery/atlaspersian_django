from rest_framework import serializers

from shop.models import *
from ._sub import *


__all__ = [
    'OrderReadSerializerAdmin',
]


class OrderReadSerializerAdmin(serializers.ModelSerializer):
    items = _OrderItemReadSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price_sum', 'items', 'is_canceled']

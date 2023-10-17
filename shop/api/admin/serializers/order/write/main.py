from django.db.models import Prefetch
from rest_framework import serializers

from shop.models import *
from ._sub import *
from ..read.main import OrderDetailSerializerAdmin


__all__ = [
    'OrderWriteSerializerAdmin',
]


class OrderWriteSerializerAdmin(serializers.ModelSerializer):
    items = serializers.ListSerializer(child=_OrderItemWriteSerializer(), allow_empty=False)

    class Meta:
        model = Order
        fields = [
            'user',
            'items',
            'status',
            'pay_method',
            'address',
            'ship_method',
            'is_verified',
        ]

    def to_representation(self, instance: Order) -> dict:
        return OrderDetailSerializerAdmin(instance).data

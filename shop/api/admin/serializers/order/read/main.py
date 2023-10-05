from rest_framework import serializers

from shop.models import *
from shop.api.admin.serializers import UserReadSerializerAdmin
from ._sub import *


__all__ = [
    'OrderReadSerializerAdmin',
]


class OrderReadSerializerAdmin(serializers.ModelSerializer):
    user = UserReadSerializerAdmin(read_only=True)

    items = _OrderItemReadSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'number',
            'user',
            'status',
            'pay_method',
            'pay_amount',
            'address',
            'ship_method',
            'user_note',
            'is_verified',
            'created_at',
            'updated_at',
        ]

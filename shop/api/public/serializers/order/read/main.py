from rest_framework import serializers

from shop.models import *
from ._sub import _OrderItemSerializer, _PaymentMethodSerializer, _AddressSerializer


__all__ = [
    'OrderListSerializerPublic',
    'OrderDetailSerializerPublic',
]


class OrderListSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'number',
            'status',
            'pay_method',
            'pay_amount',
            'address',
            'is_verified',
        ]


class OrderDetailSerializerPublic(serializers.ModelSerializer):
    pay_method = _PaymentMethodSerializer(read_only=True)
    address = _AddressSerializer(read_only=True)

    items = _OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            'number',
            'status',
            'pay_method',
            'pay_amount',
            'address',
            'user_note',
            'is_verified',
            'items'
        ]

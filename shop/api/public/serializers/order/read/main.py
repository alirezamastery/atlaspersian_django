from rest_framework import serializers

from shop.models import *
from ._sub import (
    _OrderItemSerializer,
    _PaymentMethodSerializer,
    _AddressSerializer,
    _ShippingMethodSerializer
)


__all__ = [
    'OrderListSerializerPublic',
    'OrderDetailSerializerPublic',
]


class OrderListSerializerPublic(serializers.ModelSerializer):
    pay_method = _PaymentMethodSerializer(read_only=True)
    ship_method = _ShippingMethodSerializer(read_only=True)
    address = _AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'number',
            'status',
            'pay_method',
            'ship_method',
            'address',
            'user_note',
            'is_verified',
            'shipping_cost',
            'pay_amount',
            'created_at',
        ]


class OrderDetailSerializerPublic(serializers.ModelSerializer):
    pay_method = _PaymentMethodSerializer(read_only=True)
    ship_method = _ShippingMethodSerializer(read_only=True)
    address = _AddressSerializer(read_only=True)

    items = _OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'number',
            'status',
            'pay_method',
            'ship_method',
            'address',
            'user_note',
            'is_verified',
            'shipping_cost',
            'pay_amount',
            'created_at',
            'items'
        ]

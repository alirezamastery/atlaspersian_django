from django.db.models import Prefetch
from rest_framework import serializers

from shop.models import *
from ..read.main import OrderDetailSerializerPublic
from ._sub import _OrderItemWriteSerializer


__all__ = [
    'OrderWriteSerializerPublic',
]


class OrderWriteSerializerPublic(serializers.ModelSerializer):
    items = serializers.ListSerializer(child=_OrderItemWriteSerializer(), allow_empty=False)

    class Meta:
        model = Order
        fields = [
            'pay_method'
            'address',
            'user_note',
            'items',
        ]

    def create(self, validated_data):
        request = self.context.get('request')

        items = validated_data['items']
        pay_method = validated_data['pay_method']
        address = validated_data['pay_method']

        pay_amount = sum(item['quantity'] * item['variant'].price for item in items)
        order = Order.objects.create(
            user=request.user,
            pay_amount=pay_amount,
            pay_method=pay_method,
            address=address
        )

        for item in items:
            variant = item['variant']
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                item=variant,
                price=variant.price,
                quantity=quantity
            )
            variant.inventory = variant.inventory - quantity
            variant.save()

        prefetch_items = Prefetch(
            'items',
            queryset=OrderItem.objects.all()
            .select_related('item__product__brand')
            .order_by('id')
        )
        order = (Order.objects
                 .select_related('pay_method')
                 .select_related('address__province')
                 .select_related('address__city')
                 .prefetch_related(prefetch_items)
                 .get(id=order.id))

        return order

    def to_representation(self, instance: Order) -> dict:
        return OrderDetailSerializerPublic(instance).data

from django.db.models import Prefetch, F
from rest_framework import serializers

from shop.models import *
from ..read.main import OrderDetailSerializerPublic
from ._sub import _OrderItemWriteSerializer
from utils.drf.error_codes import *


__all__ = [
    'OrderWriteSerializerPublic',
]


class OrderWriteSerializerPublic(serializers.ModelSerializer):
    items = serializers.ListSerializer(child=_OrderItemWriteSerializer(), allow_empty=False)

    class Meta:
        model = Order
        fields = [
            'items',
            'pay_method'
            'ship_method'
            'address',
            'user_note',
        ]

    def validate(self, attrs):
        items = attrs['items']
        for item in items:
            variant = item['variant']
            quantity = item['quantity']
            if quantity > variant.inventory:
                raise serializers.ValidationError({
                    'code':       APIErrorCodes.INVALID_VARIANT_QUANTITY.value,
                    'variant_id': variant.id,
                    'inventory':  variant.inventory,
                })

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')

        items = validated_data['items']
        pay_method = validated_data['pay_method']
        ship_method = validated_data['ship_method']
        address = validated_data['pay_method']

        pay_amount = ship_method.cost
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
                variant=variant,
                quantity=quantity,
                discount_percent=variant.discount_percent,
                raw_price=variant.raw_price,
                selling_price=variant.selling_price,
            )
            variant.inventory = F('inventory') - quantity
            variant.sale_count = F('sale_count') + quantity
            variant.save()

            pay_amount += variant.selling_price * quantity

        order.pay_amount = pay_amount
        order.save()

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

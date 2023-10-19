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
    discount_code = serializers.CharField()

    class Meta:
        model = Order
        fields = [
            'items',
            'pay_method',
            'ship_method',
            'address',
            'user_note',
            'discount_code',
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

        code = attrs.get('discount_code')
        print(f'{code = }')
        try:
            code_obj = DiscountCode.objects.get(code=code)
        except DiscountCode.DoesNotExist:
            code_obj = None
        attrs['discount_code_obj'] = code_obj

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')

        items = validated_data['items']
        pay_method = validated_data['pay_method']
        ship_method = validated_data['ship_method']
        address = validated_data['address']
        user_note = validated_data['user_note']
        discount_code_obj = validated_data['discount_code_obj']

        pay_amount = 0
        order = Order.objects.create(
            user=request.user,
            user_note=user_note,
            discount_code=discount_code_obj,
            pay_amount=pay_amount,
            pay_method=pay_method,
            address=address,
            ship_method=ship_method,
            shipping_cost=ship_method.cost,
        )

        for item in items:
            variant = item['variant']
            quantity = item['quantity']

            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=quantity,
                discount_percent=variant.discount_percent,
                discount_value=variant.discount_value,
                raw_price=variant.raw_price,
                selling_price=variant.selling_price,
            )
            variant.inventory = F('inventory') - quantity
            variant.sale_count = F('sale_count') + quantity
            variant.save()

            pay_amount += variant.selling_price * quantity
            print(f'{pay_amount = }')

        print(f'{discount_code_obj = }')
        if discount_code_obj is not None:
            pay_amount = discount_code_obj.apply_discount(pay_amount)
            print(f'apply_discount: {pay_amount = }')
        pay_amount += ship_method.cost
        print(f'{pay_amount = }')
        order.pay_amount = pay_amount
        order.save()

        prefetch_items = Prefetch(
            'items',
            queryset=OrderItem.objects.all()
            .select_related('variant__product__brand')
            .order_by('id')
        )
        order = (Order.objects
                 .select_related('pay_method')
                 .select_related('ship_method')
                 .select_related('address__province', 'address__city')
                 .prefetch_related(prefetch_items)
                 .get(id=order.id))

        return order

    def to_representation(self, instance: Order) -> dict:
        return OrderDetailSerializerPublic(instance).data

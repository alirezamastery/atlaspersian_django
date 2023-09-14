from rest_framework.serializers import ModelSerializer

from shop.models import *
from users.models import *


class _PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'type',
            'title',
            'description',
        ]


class _Province(ModelSerializer):
    class Meta:
        model = Province
        fields = ['title']


class _City(ModelSerializer):
    class Meta:
        model = City
        fields = ['title']


class _AddressSerializer(ModelSerializer):
    province = _Province(read_only=True)
    city = _City(read_only=True)

    class Meta:
        model = Address
        fields = [
            'title',
            'postal_code',
            'province',
            'city',
            'address',
        ]


class _SelectorType(ModelSerializer):
    class Meta:
        model = SelectorType
        fields = ['title', 'code']


class _SelectorValue(ModelSerializer):
    type = _SelectorType(read_only=True)

    class Meta:
        model = SelectorValue
        fields = [
            'type',
            'title',
            'value',
            'extra_info',
        ]


class _Brand(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


class _Product(ModelSerializer):
    brand = _Brand(read_only=True)

    class Meta:
        model = Product
        fields = [
            'brand',
            'title',
            'description',
            'thumbnail',
        ]


class _Variant(ModelSerializer):
    selector_value = _SelectorValue(read_only=True)
    product = _Product(read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'product', 'selector_value']


class _OrderItemSerializer(ModelSerializer):
    item = _Variant(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item', 'price', 'quantity']
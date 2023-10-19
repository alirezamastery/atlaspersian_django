from rest_framework.serializers import ModelSerializer

from shop.models import *


__all__ = [
    'DiscountCodeReadSerializerAdmin',
    'DiscountCodeWriteSerializerAdmin',
]


class DiscountCodeReadSerializerAdmin(ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = [
            'id',
            'code',
            'percent',
        ]


class DiscountCodeWriteSerializerAdmin(ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = [
            'code',
            'percent',
        ]

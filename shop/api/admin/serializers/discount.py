from rest_framework.serializers import ModelSerializer, ValidationError

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
            'type',
            'code',
            'value',
        ]


class DiscountCodeWriteSerializerAdmin(ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = [
            'type',
            'code',
            'value',
        ]

    def validate(self, attrs):
        value = attrs.get('value')
        if attrs.get('type') == DiscountCode.Types.PERCENT and value > 99:
            raise ValidationError('invalid percent')
        return attrs

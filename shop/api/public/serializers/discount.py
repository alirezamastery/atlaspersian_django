from rest_framework import serializers

from shop.models import *
from utils.drf.error_codes import *


__all__ = [
    'DiscountCodeVerifySerializerPublic',
]


class DiscountCodeVerifySerializerPublic(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        code = attrs.get('code')
        try:
            code_obj = DiscountCode.objects.get(code=code)
        except DiscountCode.DoesNotExist:
            raise serializers.ValidationError({
                'message': 'invalid discount code',
                'code':    APIErrorCodes.INVALID_DISCOUNT_CODE.value
            })
        attrs['code_obj'] = code_obj
        return attrs

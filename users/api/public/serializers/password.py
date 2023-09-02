from rest_framework import serializers

from users.models import *
from utils.drf.codes import *


__all__ = [
    'UserMobileSerializer',
    'ChangePasswordSerializer',
]


class UserMobileSerializer(serializers.Serializer):
    mobile = serializers.CharField()

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if not User.objects.filter(mobile=mobile, is_active=True).exists():
            raise serializers.ValidationError({
                'code':    APIErrorCodes.MOBILE_NOT_REGISTERED.value,
                'message': 'otp expired'
            })
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=20, trim_whitespace=True)

import re
import datetime as dt

from rest_framework import serializers

from users.models import *
from utils.logging import logger
from utils.drf.codes import *


__all__ = [
    'MobileSerializer',
    'OtpVerifySerializer',
]


class MobileSerializer(serializers.Serializer):
    mobile = serializers.CharField()

    @staticmethod
    def validate_mobile(data):
        if re.match(r'^09\d{9}$', data):
            return data
        raise serializers.ValidationError({
            'code':    APIErrorCodes.INVALID_MOBILE.value,
            'message': 'invalid mobile'
        })


class OtpVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField()
    code = serializers.CharField()

    @staticmethod
    def validate_mobile(data):
        if re.match(r'^09\d{9}$', data):
            return data
        raise serializers.ValidationError({
            'code':    APIErrorCodes.INVALID_MOBILE.value,
            'message': 'invalid mobile'
        })

    @staticmethod
    def validate_otp(data):
        if re.match(r'^\d{5,6}$', data):
            return data
        raise serializers.ValidationError({
            'code':    APIErrorCodes.INVALID_OTP.value,
            'message': 'invalid otp'
        })

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.get('code')

        try:
            otp = OTP.objects.get(mobile=mobile, code=code)
        except OTP.DoesNotExist:
            raise serializers.ValidationError({
                'code':    APIErrorCodes.INVALID_OTP.value,
                'message': 'invalid otp'
            })
        print(otp.created_at)
        print(dt.datetime.now())
        print(dt.datetime.now(dt.timezone.utc) - otp.created_at)
        if dt.datetime.now(dt.timezone.utc) - otp.created_at > dt.timedelta(minutes=15):
            raise serializers.ValidationError({
                'code':    APIErrorCodes.OTP_EXPIRED.value,
                'message': 'otp expired'
            })

        return attrs

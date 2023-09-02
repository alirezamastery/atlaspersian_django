import re
import datetime as dt

from rest_framework import serializers

from users.models import *
from utils.logging import logger
from utils.drf.codes import *


__all__ = [
    'NewMobileOtpSerializer',
    'SignupSerializer',
    'OtpVerifySerializer',
]


class NewMobileOtpSerializer(serializers.Serializer):
    mobile = serializers.CharField()

    @staticmethod
    def validate_mobile(data):
        if re.match(r'^09[\d]{9}$', data):
            return data
        raise serializers.ValidationError({
            'code':    APIErrorCodes.INVALID_MOBILE.value,
            'message': 'invalid mobile'
        })

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if User.objects.filter(mobile=mobile, is_active=True).exists():
            raise serializers.ValidationError({
                'code':    APIErrorCodes.MOBILE_ALREADY_EXISTS.value,
                'message': 'user with this mobile exists'
            })
        return attrs


class SignupSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField(
        max_length=20,
        min_length=6,
        trim_whitespace=True
    )

    @staticmethod
    def validate_mobile(data):
        if re.match(r'^09[\d]{9}$', data):
            return data
        raise serializers.ValidationError({
            'code':    APIErrorCodes.INVALID_MOBILE.value,
            'message': 'invalid mobile'
        })

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if User.objects.filter(mobile=mobile, is_active=True).exists():
            raise serializers.ValidationError({
                'code':    APIErrorCodes.MOBILE_ALREADY_EXISTS.value,
                'message': 'user with this mobile exists'
            })
        return attrs

    def create(self, validated_data):
        mobile = validated_data.get('mobile')
        password = validated_data.get('password')  # TODO: change to otp login
        User.objects.filter(mobile=mobile, is_active=False).delete()
        user = User.objects.create_user(mobile=mobile, password=password)

        return user


class OtpVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField()
    code = serializers.IntegerField()

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        logger(f'validate: {mobile = } {code = }')
        try:
            otp = UserOTP.objects.select_related('user').get(user__mobile=mobile, code=code)
            if dt.datetime.now() - otp.created_at > dt.timedelta(minutes=15):
                raise serializers.ValidationError({
                    'code':    APIErrorCodes.OTP_EXPIRED.value,
                    'message': 'otp expired'
                })

        except UserOTP.DoesNotExist:
            raise serializers.ValidationError({
                'code':    APIErrorCodes.INVALID_OTP.value,
                'message': 'invalid otp'
            })

        attrs['user'] = otp.user

        return attrs

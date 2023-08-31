from rest_framework import serializers

from users.models import User


__all__ = [
    'SignupSerializer',
    'ChangePasswordSerializer',
    'PasswordResetSerializer',
]


class SignupSerializer(serializers.Serializer):
    mobile = serializers.CharField(min_length=10, max_length=12)
    password = serializers.CharField(min_length=6, max_length=20)


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(min_length=10, max_length=12)
    password = serializers.CharField(min_length=6, max_length=20)


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=20, trim_whitespace=True)


class PasswordResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(min_length=6, max_length=20, trim_whitespace=True)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        try:
            attrs['user'] = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'no user with id: {user_id}')
        return attrs

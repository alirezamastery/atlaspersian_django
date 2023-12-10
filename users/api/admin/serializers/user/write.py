from rest_framework import serializers

from users.models import User
from .read.main import UserReadSerializerAdmin


__all__ = [
    'UserWriteSerializerAdmin',
    'PasswordResetSerializer',
]


class UserWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'mobile',
            'is_staff',
            'is_active',
            'is_superuser',
            'user_permissions',
            'groups'
        ]

    def to_representation(self, instance):
        return UserReadSerializerAdmin(instance).data


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=20, trim_whitespace=True)

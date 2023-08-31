from rest_framework import serializers

from users.models import User
from .read.main import UserReadSerializerPublic


__all__ = [
    'UserWriteSerializerPublic'
]


class UserWriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'mobile',
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'user_permissions',
            'groups'
        ]

    def to_representation(self, instance):
        return UserReadSerializerPublic(instance).data

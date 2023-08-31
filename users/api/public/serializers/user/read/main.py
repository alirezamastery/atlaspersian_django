from rest_framework import serializers

from users.models import User

from ._sub import _ProfileSerializer


__all__ = [
    'UserReadSerializerPublic'
]


class UserReadSerializerPublic(serializers.ModelSerializer):
    profile = _ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'mobile',
            'is_active',
            'is_superuser',
            'verified_at',
            'created_at',
            'updated_at',
            'profile',
            'groups'
        ]

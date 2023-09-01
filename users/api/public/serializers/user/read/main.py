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
            'mobile',
            'profile',
        ]

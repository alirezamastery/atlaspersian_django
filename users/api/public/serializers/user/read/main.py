from rest_framework.serializers import ModelSerializer

from users.models import User

from ._sub import _ProfileSerializer, _ProfilePublicInfoSerializer


__all__ = [
    'UserReadSerializerPublic',
    'UserPublicInfoSerializer',
]


class UserReadSerializerPublic(ModelSerializer):
    profile = _ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'mobile',
            'profile',
        ]


class UserPublicInfoSerializer(ModelSerializer):
    profile = _ProfilePublicInfoSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'profile'
        ]

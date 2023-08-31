from rest_framework import serializers

from users.models import Address


__all__ = [
    'AddressReadSerializerPublic',
]


class AddressReadSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'user',
            'title',
            'province',
            'city',
            'details',
        ]

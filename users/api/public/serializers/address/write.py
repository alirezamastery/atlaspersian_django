from rest_framework import serializers

from users.models import Address


__all__ = [
    'AddressCreateSerializerPublic',
    'AddressUpdateSerializerPublic',
]


class AddressCreateSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'title',
            'province',
            'city',
            'details',
        ]


class AddressUpdateSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'title',
            'province',
            'city',
            'details',
        ]

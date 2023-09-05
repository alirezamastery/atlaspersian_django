from rest_framework import serializers

from users.models import *


__all__ = [
    'AddressReadSerializerPublic',
    'ProvinceReadSerializerPublic',
    'CityReadSerializerPublic',
]


class AddressReadSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'title',
            'postal_code',
            'province',
            'city',
            'details',
        ]


class ProvinceReadSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = [
            'id',
            'title',
        ]


class CityReadSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            'province',
            'title',
        ]

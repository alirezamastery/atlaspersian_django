from rest_framework import serializers

from users.models import *


__all__ = [
    'AddressReadSerializerPublic',
    'ProvinceReadSerializerPublic',
    'CityReadSerializerPublic',
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


class AddressReadSerializerPublic(serializers.ModelSerializer):
    province = ProvinceReadSerializerPublic(read_only=True)
    city = CityReadSerializerPublic(read_only=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'title',
            'postal_code',
            'province',
            'city',
            'address',
        ]

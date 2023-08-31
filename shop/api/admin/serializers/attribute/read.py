from rest_framework import serializers

from shop.models import Attribute, AttributeUnit


__all__ = [
    'AttributeReadSerializerAdmin',
]


class _AttributeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeUnit
        fields = ['id', 'title']


class AttributeReadSerializerAdmin(serializers.ModelSerializer):
    unit = _AttributeUnitSerializer(read_only=True)

    class Meta:
        model = Attribute
        fields = [
            'id',
            'title',
            'description',
            'type',
            'unit',
        ]

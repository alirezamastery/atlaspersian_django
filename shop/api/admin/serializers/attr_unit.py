from rest_framework import serializers

from shop.models import AttributeUnit


__all__ = [
    'AttributeUnitReadWriteSerializerAdmin',
]


class AttributeUnitReadWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = AttributeUnit
        fields = [
            'id',
            'title',
        ]

from rest_framework import serializers

from shop.models import Attribute


__all__ = [
    'AttributeWriteSerializerAdmin',
]


class AttributeWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = [
            'title',
            'description',
            'type',
            'unit',
        ]

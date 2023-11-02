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

    def validate(self, attrs):
        title = attrs.get('title')
        unit = attrs.get('unit')

        if Attribute.objects.filter(title=title, unit=unit).exists():
            raise serializers.ValidationError('already exists')

        return attrs

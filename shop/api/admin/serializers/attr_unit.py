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

    def validate(self, attrs):
        title = attrs.get('title')

        if AttributeUnit.objects.filter(title=title).exists():
            raise serializers.ValidationError('already exists')

        return attrs

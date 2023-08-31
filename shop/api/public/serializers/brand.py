from rest_framework import serializers

from shop.models import Brand


__all__ = [
    'BrandReadSerializerPublic',
]


class BrandReadSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']

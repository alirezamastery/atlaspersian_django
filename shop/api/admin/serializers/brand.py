from rest_framework import serializers

from shop.models import Brand


__all__ = [
    'BrandReadWriteSerializerAdmin',
]


class BrandReadWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']

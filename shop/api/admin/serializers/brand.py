from rest_framework import serializers

from shop.models import *


__all__ = [
    'BrandReadWriteSerializerAdmin',
    'BrandWriteSerializerAdmin',
    'BrandReadSerializerAdmin',
]


class BrandReadWriteSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


class BrandReadSerializerAdmin(serializers.ModelSerializer):
    class _CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['id', 'title']

    categories = _CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Brand
        fields = ['id', 'title', 'categories']


class BrandWriteSerializerAdmin(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Brand
        fields = ['title', 'categories']

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from shop.models import *
from ._sub import (
    _BrandSerializer,
    _CategorySerializer,
    _AttributeValueSerializer,
    _VariantSerializer,
    _ImageSerializer
)


__all__ = [
    'ProductListSerializerAdmin',
    'ProductDetailSerializerAdmin',
]


class ProductListSerializerAdmin(serializers.ModelSerializer):
    brand = _BrandSerializer(read_only=True)
    category = _CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'thumbnail',
            'score',
            'category',
            'variants',
            'created_at',
            'updated_at'
        ]


class ProductDetailSerializerAdmin(serializers.ModelSerializer):
    brand = _BrandSerializer(read_only=True)
    category = _CategorySerializer(read_only=True)
    attribute_values = _AttributeValueSerializer(read_only=True, many=True)
    variants = _VariantSerializer(read_only=True, many=True)
    images = serializers.SerializerMethodField(method_name='get_images')

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'slug',
            'thumbnail',
            'score',
            'category',
            'attribute_values',
            'variants',
            'images',
            'created_at',
            'updated_at'
        ]

    @extend_schema_field(_ImageSerializer)
    def get_images(self, obj: Product):
        images = obj.images.all().order_by('-is_main')
        return _ImageSerializer(images, many=True, context=self.context).data

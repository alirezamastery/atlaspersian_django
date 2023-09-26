from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from shop.models import *
from ._sub import (
    _BrandSerializer,
    _CategorySerializer,
    _VariantSerializer,
    _AttributeValueSerializer,
    _ImageSerializer,
    _QuestionSerializer,
)


__all__ = [
    'ProductListSerializerPublic',
    'ProductDetailSerializerPublic',
]


class ProductListSerializerPublic(serializers.ModelSerializer):
    brand = _BrandSerializer(read_only=True)
    category = _CategorySerializer(read_only=True)
    variants = _VariantSerializer(read_only=True, many=True)
    price_min = serializers.IntegerField()

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
            'category',
            'variants',
            'price_min',
            'score',
        ]


class ProductDetailSerializerPublic(serializers.ModelSerializer):
    brand = _BrandSerializer(read_only=True)
    category = _CategorySerializer(read_only=True)
    attribute_values = _AttributeValueSerializer(read_only=True, many=True)
    variants = _VariantSerializer(read_only=True, many=True)
    images = serializers.SerializerMethodField(method_name='get_images')
    questions = _QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'slug',
            'thumbnail',
            'category',
            'attribute_values',
            'variants',
            'images',
            'questions',
        ]

    @extend_schema_field(_ImageSerializer)
    def get_images(self, obj: Product):
        images = obj.images.all().order_by('-is_main')
        return _ImageSerializer(images, many=True, context=self.context).data

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from shop.models import *
from ._sub import (
    _BrandSerializer,
    _CategorySerializer,
    _VariantSerializer,
    _AttributeValueSerializer,
    _ImageSerializer,
    _CommentSerializer,
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
    max_discount = serializers.IntegerField()

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
            'max_discount',
        ]

    def to_representation(self, instance):
        res = super().to_representation(instance)

        res['price_min_display'] = res['price_min'] // 10

        return res


class ProductDetailSerializerPublic(serializers.ModelSerializer):
    brand = _BrandSerializer(read_only=True)
    category = _CategorySerializer(read_only=True)

    attribute_values = _AttributeValueSerializer(read_only=True, many=True)
    variants = _VariantSerializer(read_only=True, many=True)
    images = serializers.SerializerMethodField(method_name='get_images')
    comments = _CommentSerializer(read_only=True, many=True)
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
            'comments',
            'questions',
        ]

    @extend_schema_field(_ImageSerializer)
    def get_images(self, obj: Product):
        images = obj.images.all().order_by('-is_main')
        return _ImageSerializer(images, many=True, context=self.context).data

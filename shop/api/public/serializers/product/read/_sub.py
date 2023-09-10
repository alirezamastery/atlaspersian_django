from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import *


class _BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title']


class _ImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_absolute_url')

    class Meta:
        model = ProductImage
        fields = [
            # 'product', # product is not product_id, it is the Product Object!
            'url',
            'is_main',
            'description'
        ]

    def get_absolute_url(self, obj):
        if not obj.file:
            return None
        url = obj.file.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        if (host := self.context.get('host')) is not None:
            return f'{host}{url}'
        return url


class _AttributeValueSerializer(ModelSerializer):
    class _AttributeSerializer(ModelSerializer):
        class Meta:
            model = Attribute
            fields = ['title', 'description', 'type', 'unit']

    attribute = _AttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'value', 'extra_info']


class _SelectorTypeSerializer(ModelSerializer):
    class Meta:
        model = SelectorType
        fields = ['title', 'code']


class _SelectorValueSerializer(ModelSerializer):
    type = _SelectorTypeSerializer(read_only=True)

    class Meta:
        model = SelectorValue
        fields = [
            'type',
            'title',
            'value',
            'extra_info',
        ]


class _ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'thumbnail',
        ]


class _VariantSerializer(ModelSerializer):
    selector_value = _SelectorValueSerializer(read_only=True)
    product = _ProductSerializer(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'price',
            'inventory',
            'max_in_order',
        ]


class _CategorySerializer(ModelSerializer):
    selector_type = _SelectorTypeSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type']

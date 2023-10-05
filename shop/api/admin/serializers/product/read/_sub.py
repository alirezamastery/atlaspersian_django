from rest_framework import serializers

from shop.models import *


class _BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class _ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_absolute_url')

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'url',
            'is_main',
            'description',
            'alt',
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


class _AttributeSerializer(serializers.ModelSerializer):
    class _AttributeUnitSerializer(serializers.ModelSerializer):
        class Meta:
            model = AttributeUnit
            fields = ['id', 'title']

    unit = _AttributeUnitSerializer(read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'title', 'description', 'type', 'unit']


class _AttributeValueSerializer(serializers.ModelSerializer):
    attribute = _AttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = [
            'id',
            'attribute',
            'value',
            'extra_info',
            'created_at',
            'updated_at',
        ]


class _SelectorValueSerializer(serializers.ModelSerializer):
    class _SelectorTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = SelectorType
            fields = [
                'id',
                'title',
                'code',
            ]

    type = _SelectorTypeSerializer(read_only=True)

    class Meta:
        model = SelectorValue
        fields = [
            'id',
            'type',
            'title',
            'value',
            'extra_info',
        ]


class _VariantSerializer(serializers.ModelSerializer):
    selector_value = _SelectorValueSerializer(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'is_active',
            'inventory',
            'max_in_order',
            'discount_percent',
            'raw_price',
            'selling_price',
            'sale_count',
        ]


class _CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type']

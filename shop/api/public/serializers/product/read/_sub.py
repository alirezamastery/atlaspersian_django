from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import *
from shop.api.public.serializers import UserPublicInfoSerializer


class _BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']


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


class _AttributeUnit(ModelSerializer):
    class Meta:
        model = AttributeUnit
        fields = ['title']


class _Attribute(ModelSerializer):
    unit = _AttributeUnit(read_only=True)

    class Meta:
        model = Attribute
        fields = ['title', 'description', 'type', 'unit']


class _AttributeValueSerializer(ModelSerializer):
    attribute = _Attribute(read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'value', 'extra_info']


class _SelectorType(ModelSerializer):
    class Meta:
        model = SelectorType
        fields = ['title', 'code']


class _SelectorValueSerializer(ModelSerializer):
    type = _SelectorType(read_only=True)

    class Meta:
        model = SelectorValue
        fields = [
            'type',
            'title',
            'value',
            'extra_info',
        ]


class _Product(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'thumbnail',
        ]


class _VariantSerializer(ModelSerializer):
    selector_value = _SelectorValueSerializer(read_only=True)
    product = _Product(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'price',
            'inventory',
            'max_in_order',
            'discount',
        ]


class _CategorySerializer(ModelSerializer):
    selector_type = _SelectorType(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'selector_type']


class _CommentSerializer(ModelSerializer):
    user = UserPublicInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'user',
            'text',
            'created_at',
        ]


class _QuestionSerializer(ModelSerializer):
    user = UserPublicInfoSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            'user',
            'question',
            'answer',
            'created_at',
        ]

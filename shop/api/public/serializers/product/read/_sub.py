from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import *
from shop.api.public.serializers import UserPublicInfoSerializer
from shop.utils import *


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
            'id',
            'title',
            'description',
            'thumbnail',
            'slug',
        ]


class _VariantSerializer(ModelSerializer):
    selector_value = _SelectorValueSerializer(read_only=True)
    product = _Product(read_only=True)

    price_display = serializers.IntegerField(read_only=True)

    class Meta:
        model = Variant
        fields = [
            'id',
            'product',
            'selector_value',
            'price',
            'price_display',
            'inventory',
            'max_in_order',
            'discount',
        ]

    def to_representation(self, instance):
        res = super().to_representation(instance)

        res['price_display'] = res['price'] // 10

        res['final_price'] = get_variant_final_price(instance)
        res['final_price_display'] = res['final_price'] // 10

        res['tax'] = get_variant_tax(instance)
        res['tax_display'] = res['tax'] // 10

        res['taxed_price'] = res['tax'] + res['final_price']
        res['taxed_price_display'] = res['taxed_price'] // 10

        res['discount_value'] = res['price'] - res['final_price']
        res['discount_value_display'] = res['discount_value'] // 10

        return res


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

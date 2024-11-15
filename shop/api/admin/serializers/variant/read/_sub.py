from rest_framework import serializers

from shop.models import *


class _ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'brand',
            'title',
            'description',
            'is_active',
            'thumbnail',
            'slug',
            'category',
        ]


class _VariantSelectorValueReadSerializer(serializers.ModelSerializer):
    class _VariantSelectorTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = SelectorType
            fields = ['id', 'title', 'code']

    type = _VariantSelectorTypeSerializer(read_only=True)

    class Meta:
        model = SelectorValue
        fields = ['id', 'type', 'title', 'value', 'extra_info']

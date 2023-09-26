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
            'slug',
            'thumbnail',
            'score',
        ]

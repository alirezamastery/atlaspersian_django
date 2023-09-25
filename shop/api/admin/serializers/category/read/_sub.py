from rest_framework.serializers import ModelSerializer

from shop.models import *


class _Unit(ModelSerializer):
    class Meta:
        model = AttributeUnit
        fields = ['title']


class _AttributeSerializer(ModelSerializer):
    unit = _Unit(read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'title', 'description', 'type', 'unit']


class _BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']

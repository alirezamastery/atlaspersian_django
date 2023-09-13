from rest_framework import serializers

from shop.models import *


class _ProductAttributeValueWriteSerializer(serializers.Serializer):
    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())
    value = serializers.CharField()

    class Meta:
        fields = ['attribute', 'value']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class _NewProductImageWriteSerializer(serializers.Serializer):
    file = serializers.CharField()
    is_main = serializers.BooleanField()
    description = serializers.CharField(allow_blank=True)
    alt = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

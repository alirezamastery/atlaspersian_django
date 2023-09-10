from rest_framework import serializers

from shop.models import *
from utils.drf.error_codes import APIErrorCodes


class _OrderItemWriteSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all())
    quantity = serializers.IntegerField()

    class Meta:
        fields = ['variant', 'quantity']

    def validate(self, attrs):
        variant = attrs['variant']
        quantity = attrs['quantity']
        if quantity > variant.inventory:
            raise serializers.ValidationError({'code': APIErrorCodes.INVALID_VARIANT_QUANTITY.value})
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

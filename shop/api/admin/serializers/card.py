from rest_framework import serializers


__all__ = [
    'CardInfoWriteSerializer',
]


class CardInfoWriteSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=255)
    card_owner = serializers.CharField(max_length=255)

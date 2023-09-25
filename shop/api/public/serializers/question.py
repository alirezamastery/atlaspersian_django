from rest_framework import serializers

from shop.models import *


__all__ = [
    'QuestionWriteSerializerPublic',
]


class QuestionWriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'product',
            'text',
        ]

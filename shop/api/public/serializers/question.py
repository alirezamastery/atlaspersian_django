from rest_framework import serializers

from shop.models import *


__all__ = [
    'QuestionWriteSerializerPublic',
]


class QuestionWriteSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'product',
            'question',
            'is_private',
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        q = Question.objects.create(
            user=request.user,
            product=validated_data['product'],
            question=validated_data['question']
        )
        return q

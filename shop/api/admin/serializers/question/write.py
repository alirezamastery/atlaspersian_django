from rest_framework import serializers

from shop.models import *


__all__ = [
    'QuestionUpdateSerializerAdmin',
]


class QuestionUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question',
            'answer',
            'accepted',
        ]

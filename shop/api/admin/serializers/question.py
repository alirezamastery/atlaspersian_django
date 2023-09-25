from rest_framework import serializers

from shop.models import *
from shop.api.admin.serializers import UserReadSerializerAdmin


__all__ = [
    'QuestionReadSerializerAdmin',
    'QuestionUpdateSerializerAdmin',
]


class QuestionReadSerializerAdmin(serializers.ModelSerializer):
    user = UserReadSerializerAdmin(read_only=True)

    class Meta:
        model = Question
        fields = [
            'user',
            'product',
            'question',
            'answer',
            'accepted',
            'create_at',
            'updated_at',
        ]


class QuestionUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question',
            'answer',
            'accepted',
        ]

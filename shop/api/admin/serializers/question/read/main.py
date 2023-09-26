from rest_framework import serializers

from shop.models import *
from shop.api.admin.serializers import UserReadSerializerAdmin
from ._sub import _ProductSerializer


__all__ = [
    'QuestionReadSerializerAdmin',
]


class QuestionReadSerializerAdmin(serializers.ModelSerializer):
    user = UserReadSerializerAdmin(read_only=True)
    product = _ProductSerializer(read_only=True)

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

from rest_framework import serializers

from shop.models import *
from shop.api.admin.serializers import UserReadSerializerAdmin
from ._sub import _ProductSerializer


__all__ = [
    'CommentReadSerializerAdmin',
]


class CommentReadSerializerAdmin(serializers.ModelSerializer):
    user = UserReadSerializerAdmin(read_only=True)
    product = _ProductSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'product',
            'text',
            'accepted',
            'quality_score',
            'worth_buy_score',
            'created_at',
            'updated_at',
        ]

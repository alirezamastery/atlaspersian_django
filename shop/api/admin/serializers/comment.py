from rest_framework import serializers

from shop.models import *
from shop.api.admin.serializers import UserReadSerializerAdmin


__all__ = [
    'CommentReadSerializerAdmin',
    'CommentUpdateSerializerAdmin',
]


class CommentReadSerializerAdmin(serializers.ModelSerializer):
    user = UserReadSerializerAdmin(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'user',
            'product',
            'text',
            'accepted',
            'create_at',
            'updated_at',
        ]


class CommentUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'accepted',
        ]

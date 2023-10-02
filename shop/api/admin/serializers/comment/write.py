from rest_framework import serializers

from shop.models import *


__all__ = [
    'CommentUpdateSerializerAdmin',
]


class CommentUpdateSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'accepted',
        ]

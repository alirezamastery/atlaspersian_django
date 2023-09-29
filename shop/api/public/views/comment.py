from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from shop.models import *
from shop.api.public.serializers.comment import CommentWriteSerializerPublic
from utils.drf.permissions import IsAuthenticated


__all__ = [
    'CommentViewSetPublic',
]


class CommentViewSetPublic(mixins.CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentWriteSerializerPublic
    permission_classes = [IsAuthenticated]

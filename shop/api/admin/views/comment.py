from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.admin.serializers import *


__all__ = [
    'CommentViewSet',
]


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = (Comment.objects
                .select_related('user__profile')
                .select_related('product')
                .all()
                .order_by('created_at'))

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CommentReadSerializerAdmin
        return CommentUpdateSerializerAdmin

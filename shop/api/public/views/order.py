from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.public.serializers import *
from utils.drf.permissions import IsAuthenticated


__all__ = [
    'OrderViewSetPublic',
]


class OrderViewSetPublic(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = Order.objects \
        .select_related('user') \
        .prefetch_related(Prefetch('items', queryset=OrderItem.objects.all())) \
        .all() \
        .order_by('id')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderReadSerializerPublic
        return OrderWriteSerializerPublic

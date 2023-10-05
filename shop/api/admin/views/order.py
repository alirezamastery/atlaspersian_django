from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.admin.serializers import *
from utils.drf.permissions import IsAdmin


__all__ = [
    'OrderViewSetAdmin',
]


class OrderViewSetAdmin(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrderReadSerializerAdmin
        return OrderWriteSerializerAdmin

    def get_queryset(self):
        if self.action == 'list':
            return (Order.objects
                    .select_related('user_profile')
                    .select_related('pay_method')
                    .select_related('address__province')
                    .select_related('address__city')
                    .filter(user=self.request.user)
                    .order_by('-created_at'))

        prefetch_items = Prefetch(
            'items',
            queryset=OrderItem.objects.all()
            .select_related('item__product__brand')
            .order_by('id')
        )
        return (Order.objects
                .select_related('user_profile')
                .select_related('pay_method')
                .select_related('address__province')
                .select_related('address__city')
                .prefetch_related(prefetch_items)
                .all())

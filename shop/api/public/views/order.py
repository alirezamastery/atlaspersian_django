from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS, BasePermission

from shop.models import *
from shop.api.public.serializers import *
from utils.drf.permissions import IsAuthenticated


__all__ = [
    'OrderViewSetPublic',
]


class IsOrderOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class OrderViewSetPublic(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    permission_classes = [IsAuthenticated, IsOrderOwner]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializerPublic
        if self.request.method in SAFE_METHODS:
            return OrderDetailSerializerPublic
        return OrderWriteSerializerPublic

    def get_queryset(self):
        if self.action == 'list':
            return (Order.objects
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
                .select_related('pay_method')
                .select_related('address__province')
                .select_related('address__city')
                .prefetch_related(prefetch_items)
                .all())

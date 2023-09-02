from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import mixins

from users.models import Address
from users.api.public.serializers import *


__all__ = [
    'AddressViewSetPublic'
]


class IsAddressOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class AddressViewSetPublic(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    queryset = Address.objects.all().order_by('-id')
    permission_classes = [IsAddressOwner]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AddressReadSerializerPublic

        elif self.request.method == 'PATCH':
            return AddressUpdateSerializerPublic

        return AddressCreateSerializerPublic

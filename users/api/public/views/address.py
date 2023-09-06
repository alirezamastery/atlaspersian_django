from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import mixins

from users.models import *
from users.api.public.serializers import *
from users.api.public.filters.citiy import CityFilterPublic


__all__ = [
    'AddressViewSetPublic',
    'ProvinceViewSetPublic',
    'CityViewSetPublic',
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
        return AddressWriteSerializerPublic


class ProvinceViewSetPublic(ReadOnlyModelViewSet):
    queryset = Province.objects.all().order_by('id')
    serializer_class = ProvinceReadSerializerPublic
    pagination_class = None


class CityViewSetPublic(ReadOnlyModelViewSet):
    queryset = City.objects.all().order_by('id')
    serializer_class = CityReadSerializerPublic
    filterset_class = CityFilterPublic
    pagination_class = None

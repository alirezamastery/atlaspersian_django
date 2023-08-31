from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.admin.serializers import *
from shop.api.admin.filters import *
from utils.drf.mixins import GetByIdList
from utils.drf.permissions import IsAdmin


__all__ = [
    'AttributeViewSetAdmin',
    'AttributeUnitViewSetAdmin',
]


class AttributeViewSetAdmin(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet,
                            GetByIdList):
    queryset = Attribute.objects.all().order_by('id')
    filterset_class = AttributeFilterAdmin
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AttributeReadSerializerAdmin
        return AttributeWriteSerializerAdmin


class AttributeUnitViewSetAdmin(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet,
                                GetByIdList):
    queryset = AttributeUnit.objects.all().order_by('id')
    serializer_class = AttributeUnitReadWriteSerializerAdmin
    filterset_class = AttributeUnitFilterAdmin
    permission_classes = [IsAdmin]

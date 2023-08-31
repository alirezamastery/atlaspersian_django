from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework import mixins

from shop.api.admin.filters import VariantFilterAdmin
from shop.models import Variant
from shop.api.admin.serializers import VariantReadSerializerAdmin, VariantUpdateSerializerAdmin
from utils.drf.permissions import IsAdmin, ReadOnly


__all__ = [
    'VariantViewSetAdmin',
]


class VariantViewSetAdmin(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    queryset = Variant.objects \
        .select_related('product') \
        .select_related('selector_value__type') \
        .all() \
        .order_by('id')
    filterset_class = VariantFilterAdmin
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return VariantReadSerializerAdmin
        return VariantUpdateSerializerAdmin

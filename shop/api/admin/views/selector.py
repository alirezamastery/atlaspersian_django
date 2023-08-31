from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import SelectorType
from shop.api.admin.serializers import VariantSelectorTypeReadSerializerAdmin


__all__ = [
    'VariantSelectorTypeViewSetAdmin',
]


class VariantSelectorTypeViewSetAdmin(ReadOnlyModelViewSet):
    queryset = SelectorType.objects.all().order_by('id')
    serializer_class = VariantSelectorTypeReadSerializerAdmin

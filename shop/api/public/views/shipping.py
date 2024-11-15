from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from shop.models import *
from shop.api.public.serializers import ShippingMethodReadSerializerPublic


__all__ = [
    'ShippingMethodViewSetPublic',
]


class ShippingMethodViewSetPublic(ReadOnlyModelViewSet):
    queryset = ShippingMethod.objects.all().order_by('id')
    serializer_class = ShippingMethodReadSerializerPublic
    permission_classes = [IsAuthenticated]
    pagination_class = None

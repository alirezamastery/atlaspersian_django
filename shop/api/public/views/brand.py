from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Brand
from shop.api.public.serializers import *
from utils.drf.permissions import ReadOnly


__all__ = [
    'BrandViewSetPublic',
]


class BrandViewSetPublic(ReadOnlyModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandReadSerializerPublic
    permission_classes = [ReadOnly]

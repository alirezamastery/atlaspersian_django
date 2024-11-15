from rest_framework.viewsets import ModelViewSet

from shop.models import Brand
from shop.api.admin.serializers import BrandReadWriteSerializerAdmin
from shop.api.admin.filters import BrandFilterAdmin
from utils.drf.permissions import IsAdmin
from utils.drf.mixins import GetByIdList


__all__ = [
    'BrandViewSetAdmin',
]


class BrandViewSetAdmin(ModelViewSet, GetByIdList):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandReadWriteSerializerAdmin
    permission_classes = [IsAdmin]
    filterset_class = BrandFilterAdmin

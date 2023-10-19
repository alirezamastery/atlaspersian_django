from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.admin.serializers import *
from utils.drf.permissions import IsAdmin
from utils.drf.mixins import GetByIdList


__all__ = [
    'DiscountCodeViewSetAdmin',
]


class DiscountCodeViewSetAdmin(ModelViewSet, GetByIdList):
    queryset = DiscountCode.objects.all().order_by('-id')
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return DiscountCodeReadSerializerAdmin
        return DiscountCodeWriteSerializerAdmin

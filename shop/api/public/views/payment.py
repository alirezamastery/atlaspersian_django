from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.public.serializers import *


__all__ = [
    'PaymentMethodViewSetPublic',
    'PaymentViewSet',
]


class PaymentMethodViewSetPublic(ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.all().order_by('id')
    serializer_class = PaymentMethodReadSerializerPublic
    permission_classes = [IsAuthenticated]
    pagination_class = None


class PaymentViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     GenericViewSet):
    queryset = Payment.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PaymentReadSerializerPublic
        return PaymentWriteSerializerPublic

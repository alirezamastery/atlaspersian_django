from rest_framework.serializers import ModelSerializer

from shop.models import *
from ._sub import _OrderSerializer


__all__ = [
    'PaymentReadSerializerPublic',
]


class PaymentReadSerializerPublic(ModelSerializer):
    order = _OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'tracking_id',
            'method',
            'order',
            'amount',
            'date',
        ]

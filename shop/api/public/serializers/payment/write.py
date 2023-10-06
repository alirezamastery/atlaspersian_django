from rest_framework.serializers import ModelSerializer

from shop.models import *
from shop.api.public.serializers.payment.read.main import *


__all__ = [
    'PaymentWriteSerializerPublic',
]


class PaymentWriteSerializerPublic(ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'tracking_id',
            'method',
            'order',
            'amount',
            'date',
            'card_digits',
        ]

    def save(self, **kwargs):
        payment = super().save(**kwargs)
        return Payment.objects.select_related('order').get(id=payment.id)

    def to_representation(self, instance):
        return PaymentReadSerializerPublic(instance).data

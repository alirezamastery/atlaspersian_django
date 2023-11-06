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
            'amount',
            'date',
            'successful',
            'order',
            'method',
            'card_digits',
        ]

    def save(self, **kwargs):
        payment = super().save(**kwargs)
        payment = Payment.objects.select_related('order').get(id=payment.id)

        if payment.successful:
            payment.order.status = Order.Status.PROCESSING
            payment.order.save()

        return payment

    def to_representation(self, instance):
        return PaymentReadSerializerPublic(instance).data

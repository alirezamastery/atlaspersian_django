from rest_framework.serializers import ModelSerializer

from shop.models import *


class _OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'number',
        ]

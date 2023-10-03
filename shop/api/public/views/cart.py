from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Address
from users.api.public.serializers import AddressReadSerializerPublic
from shop.models import *
from shop.api.public.serializers import *
from utils.drf.permissions import IsAuthenticated
from utils.json_db import jdb


__all__ = [
    'CartCheckoutOptionsView',
]


class CartCheckoutOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        ship_methods = ShippingMethod.objects.filter(is_active=True).order_by('id')
        pay_methods = PaymentMethod.objects.filter(is_active=True).order_by('id')

        response = {
            'addresses':    AddressReadSerializerPublic(addresses, many=True).data,
            'ship_methods': ShippingMethodReadSerializerPublic(ship_methods, many=True).data,
            'pay_methods':  PaymentMethodReadSerializerPublic(pay_methods, many=True).data,
            'card_info':         {
                'number': jdb.get(jdb.keys.CARD_NUMBER.value),
                'owner':  jdb.get(jdb.keys.CARD_OWNER.value),
            }
        }

        return Response(response)

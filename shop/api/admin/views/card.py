from rest_framework.views import APIView
from rest_framework.response import Response

from shop.api.admin.serializers import CardInfoWriteSerializer
from utils.drf.permissions import IsAdmin
from utils.json_db import jdb


__all__ = [
    'CardInfoView',
]


class CardInfoView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        response = {
            'card_number': jdb.get(jdb.keys.CARD_NUMBER.value),
            'card_owner':  jdb.get(jdb.keys.CARD_OWNER.value),
        }
        return Response(response)

    def put(self, request):
        serializer = CardInfoWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jdb.bulk_set({
            jdb.keys.CARD_NUMBER.value: serializer.validated_data['card_number'],
            jdb.keys.CARD_OWNER.value:  serializer.validated_data['card_owner'],
        })
        return Response(serializer.data)

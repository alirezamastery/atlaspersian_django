from django.db.models import Prefetch
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from shop.models import *
from shop.api.public.serializers import *
from utils.drf.permissions import IsAuthenticated


__all__ = [
    'DiscountCodeVerifyView',
]


class DiscountCodeVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DiscountCodeVerifySerializerPublic(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'percent': serializer.validated_data['code_obj'].percent
        }
        return Response(response)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import *
from users.api.public.serializers import *
from utils.logging import logger


__all__ = [
    'OtpVerifyView',
]


class OtpVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OtpVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        logger(f'{user = }')
        user.is_active = True
        user.save()

        UserOTP.objects.filter(user=user).delete()

        return Response({}, status=status.HTTP_202_ACCEPTED)

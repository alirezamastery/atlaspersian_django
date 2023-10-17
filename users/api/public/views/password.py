from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import *
from users.api.public.serializers import *
from users.tasks import send_otp
from utils.otp import generate_otp


__all__ = [
    'ForgotPasswordSendOtpView',
    'ChangePasswordView',
]


class ForgotPasswordSendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserMobileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')
        user = User.objects.get(mobile=mobile)

        send_otp.delay(user.id, generate_otp())

        return Response({'info': 'verification code sent'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']
        user = request.user
        user.set_password(new_password)
        user.save()

        return Response({'info': 'password changed'}, status=status.HTTP_202_ACCEPTED)

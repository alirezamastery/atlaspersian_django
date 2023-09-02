from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import *
from users.api.public.serializers import *
from users.tasks import send_otp_sms
from utils.logging import logger


__all__ = [
    'SignupView',
    'SignupVerifyView',
    'OtpSignupView',
]


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(f'{serializer.validated_data = }')
        user = serializer.save()
        send_otp_sms.delay(user.id)
        return Response({'info': 'user created'}, status=status.HTTP_201_CREATED)


class SignupVerifyView(APIView):
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


class OtpSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MobileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')
        User.objects.create(mobile=mobile, is_active=True)

        user = User.objects.select_related('profile').get(mobile=mobile)
        serializer = UserReadSerializerPublic(user)
        login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

import uuid

from django.contrib.auth import login as auth_login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.models import *
from users.api.public.serializers import *
from users.tasks import *
from utils.logging import logger
from utils.otp import generate_otp


__all__ = [
    'SendAuthenticationOtpView',
    'VerifyAuthenticationOtpView',
]


class SendAuthenticationOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MobileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')

        response = {'existing_user': False}

        try:
            User.objects.get(mobile=mobile)
            response['existing_user'] = True
        except User.DoesNotExist:
            pass

        code = generate_otp()
        print(f'{code = }')
        OTP.objects.create(mobile=mobile, code=code)
        # send_otp.delay(mobile)

        return Response(response)


class VerifyAuthenticationOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OtpVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')

        try:
            user = User.objects.select_related('profile').get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(mobile=mobile, password=uuid.uuid4().hex)

        auth_login(request, user)

        serializer = UserReadSerializerPublic(user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

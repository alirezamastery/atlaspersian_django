from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import *
from users.api.public.serializers import *


__all__ = [
    'CSRFView',
    'UserExistView',
    'LoginView',
    'LogoutView',
    'TestCookieView',
]


class CSRFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = Response({'message': 'Set CSRF cookie'})
        response['X-CSRFToken'] = get_token(request)
        return response


class UserExistView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        try:
            User.objects.get(mobile=mobile)
            return Response({'exist': True})
        except User.DoesNotExist:
            return Response({'exist': False})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        user = authenticate(mobile=mobile, password=password)
        if user is not None:
            login(request, user)
            serializer = UserReadSerializerPublic(user)
            return Response(serializer.data)
        return Response({'error': 'invalid credentials'}, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'info': 'logged out'})


class TestCookieView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        cookie = request.COOKIES.get('csrftoken')
        print('user:', request.user)
        print('cokies:', request.COOKIES)
        return Response({'info': 'ok'})

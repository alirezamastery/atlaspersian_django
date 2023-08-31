from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


__all__ = [
    'LoginView',
    'TestCookieView',
    'CSRFView',
]


class CSRFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response = Response({'message': 'Set CSRF cookie'})
        response['X-CSRFToken'] = get_token(request)
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        user = authenticate(mobile=mobile, password=password)
        if user is not None:
            login(request, user)
            return Response({'info': 'ok'})
        return Response({'error': 'invalid credentials'}, status=400)


class TestCookieView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        cookie = request.COOKIES.get('csrftoken')
        print('user:', request.user)
        print('cokies:', request.COOKIES)
        return Response({'info': 'ok'})

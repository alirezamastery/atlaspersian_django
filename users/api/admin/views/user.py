from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action

from users.models import User
from users.api.admin.serializers import *
from users.api.admin.filters.user import UserFilterAdmin


__all__ = [
    'UserViewSetAdmin',
    'ProfileViewAdmin',
]


class UserViewSetAdmin(ModelViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilterAdmin

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserReadSerializerAdmin
        return UserWriteSerializerAdmin

    @action(methods=['GET'], detail=False, url_path='my-info')
    def my_info(self, request):
        user = (User.objects
                .select_related('profile')
                .prefetch_related('groups')
                .get(pk=request.user.id))
        serializer = UserReadSerializerAdmin(user, context={'request': request})
        return Response(serializer.data)


class ProfileViewAdmin(APIView):
    http_method_names = ['get', 'patch', 'options']

    def get(self, request):
        serializer = ProfileReadSerializerAdmin(request.user.profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileWriteSerializerAdmin(data=request.data, instance=profile, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

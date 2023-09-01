from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS

from users.models import User
from users.api.public.serializers import *


__all__ = [
    'UserViewSetPublic',
    'ProfileViewPublic',
]


class UserViewSetPublic(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserWriteSerializerPublic
        return UserReadSerializerPublic

    @action(methods=['GET'], detail=False, url_path='my-info')
    def my_info(self, request):
        user = (User.objects
                .select_related('profile')
                .get(pk=request.user.id))
        serializer = UserReadSerializerPublic(user, context={'request': request})
        return Response(serializer.data)


class ProfileViewPublic(APIView):
    http_method_names = ['get', 'patch', 'options']

    def get(self, request):
        serializer = ProfileReadSerializerPublic(request.user.profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileWriteSerializerPublic(
            data=request.data,
            instance=profile,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

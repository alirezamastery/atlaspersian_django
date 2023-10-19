from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import *
from users.api.public.serializers import *
from shop.models import Order


__all__ = [
    'UserInfoView',
    'ProfileViewPublic',
    'UserAddressListView',
]


class UserInfoView(APIView):

    def get(self, request):
        user = User.objects.select_related('profile').get(pk=request.user.id)
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


class UserAddressListView(APIView):

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressReadSerializerPublic(addresses, many=True)
        return Response(serializer.data)

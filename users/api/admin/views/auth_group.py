from django.contrib.auth.models import Group
from rest_framework.permissions import SAFE_METHODS

from rest_framework.viewsets import ModelViewSet

from users.api.admin.serializers import *
from utils.drf.permissions import *
from utils.drf.mixins import *


__all__ = [
    'AuthGroupViewSetAdmin',
]


class AuthGroupViewSetAdmin(ModelViewSet, GetByIdList):
    queryset = Group.objects.all().order_by('-id')
    permission_classes = [IsSuperuser]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuthGroupReadSerializerAdmin
        return AuthGroupWriteSerializerAdmin

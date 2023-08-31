from django.contrib.auth.models import Permission
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

from users.api.admin.serializers import *
from utils.drf.permissions import *
from utils.drf.mixins import *


__all__ = [
    'AuthPermissionViewSetAdmin',
]


class AuthPermissionViewSetAdmin(ModelViewSet, GetByIdList):
    queryset = Permission.objects.all().order_by('-id')
    permission_classes = [IsSuperuser]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuthPermissionReadSerializerAdmin
        return AuthPermissionWriteSerializerAdmin

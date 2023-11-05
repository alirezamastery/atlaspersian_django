from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS

from shop.models import *
from shop.api.admin.serializers import *
from utils.drf.permissions import *


__all__ = [
    'ImageViewSetAdmin',
    'HomeSlideViewSetAdmin',
]


class ImageViewSetAdmin(ModelViewSet):
    queryset = ProductImage.objects.all().order_by('id')
    serializer_class = ImageReadSerializer
    permission_classes = [IsAdmin]

    @action(methods=['POST'], detail=False, url_path='upload')
    def upload(self, request, *args, **kwargs):
        serializer = ImageUploadSerializerAdmin(data=request.data, context={
            'save_path': 'product/img/',
            'request':   request
        })
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response)


class HomeSlideViewSetAdmin(ModelViewSet):
    queryset = HomeSlide.objects.all().order_by('id')
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return HomeSlideReadSerializerAdmin
        return HomeSlideWriteSerializerAdmin

    @action(methods=['POST'], detail=False, url_path='upload')
    def upload(self, request, *args, **kwargs):
        serializer = ImageUploadSerializerAdmin(data=request.data, context={
            'save_path': 'home/slide/',
            'request':   request
        })
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response)

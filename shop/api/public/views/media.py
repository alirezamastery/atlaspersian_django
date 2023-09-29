from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from shop.models import *
from shop.api.public.serializers import *


__all__ = [
    'HomeSlideViewSetPublic',
]


class HomeSlideViewSetPublic(mixins.ListModelMixin, GenericViewSet):
    queryset = HomeSlide.objects.all().order_by('id')
    serializer_class = HomeSlideReadSerializerPublic
    pagination_class = None

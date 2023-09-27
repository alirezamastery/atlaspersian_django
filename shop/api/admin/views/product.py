from django.db.models import Prefetch, F
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from shop.models import *
from shop.api.admin.serializers import *
from shop.api.admin.filters import *
from utils.drf.permissions import IsAdmin


__all__ = [
    'ProductViewSetAdmin',
]


class ProductViewSetAdmin(ModelViewSet):
    permission_classes = [IsAdmin]
    filterset_class = ProductFilterAdmin

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializerAdmin
        if self.action == 'retrieve':
            return ProductDetailSerializerAdmin
        return ProductWriteSerializerAdmin

    def get_queryset(self):
        if self.action == 'list':
            return Product.objects \
                .select_related('brand') \
                .select_related('category') \
                .all() \
                .order_by('-id')

        prefetch_attrs = Prefetch(
            'attribute_values',
            queryset=ProductAttributeValue.objects.select_related('attribute__unit')
        )
        return (Product.objects
                .select_related('brand')
                .select_related('category')
                .prefetch_related('variants__selector_value__type')
                .prefetch_related(prefetch_attrs)
                .all()
                .order_by('-id'))

    @action(detail=False, methods=['POST'], url_path='add-variants')
    def add_variants(self, request, *args, **kwargs):
        serializer = VariantCreateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

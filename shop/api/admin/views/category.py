from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.models import *
from shop.api.admin.serializers import *
from shop.api.admin.filters import CategoryFilterAdmin
from utils.drf.permissions import IsAdmin


__all__ = [
    'CategoryViewSetAdmin',
]


class CategoryViewSetAdmin(ModelViewSet):
    queryset = Category.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')
    filterset_class = CategoryFilterAdmin
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCategoryListSerializer
        if self.action == 'retrieve' or self.request.method in SAFE_METHODS:
            return ProductCategoryDetailSerializer
        return ProductCategoryWriteSerializer

    @action(detail=False, methods=['GET'], url_path='get-tree')
    def get_tree(self, request):
        tree_structure = Category.dump_bulk_custom()
        return Response(tree_structure)

    # def get_paginated_response(self, data):
    #     response = super().get_paginated_response(data)
    #     if response.data['next'] is None:
    #         response.data['items'].insert(0, {
    #             'id':    0,
    #             'title': '-- سرشاخه --'
    #         })
    #     return response

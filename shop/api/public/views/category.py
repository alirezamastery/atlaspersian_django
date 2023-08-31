from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.models import *
from shop.api.public.serializers.category import *
from utils.drf.permissions import ReadOnly


__all__ = [
    'CategoryViewSetPublic',
]


class CategoryViewSetPublic(ReadOnlyModelViewSet):
    queryset = Category.objects \
        .select_related('selector_type') \
        .all() \
        .order_by('id')
    permission_classes = [ReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializerPublic
        return CategoryDetailSerializerPublic

    @action(detail=False, methods=['GET'], url_path='get-tree')
    def get_tree(self, request):
        tree_structure = Category.dump_bulk_custom()
        return Response({'tree': tree_structure})


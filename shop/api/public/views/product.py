from django.db.models import Sum, OuterRef, Subquery, Value, Prefetch, Min, Max
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from shop.models import *
from shop.api.public.serializers import *
from shop.api.public.filters import *
from utils.drf.permissions import ReadOnly


__all__ = [
    'ProductViewSetPublic',
]


class ProductViewSetPublic(ReadOnlyModelViewSet):
    filterset_class = ProductFilterPublic
    permission_classes = [ReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializerPublic
        return ProductDetailSerializerPublic

    def get_queryset(self):
        if self.action == 'list':
            prefetch_variants = Prefetch(
                'variants',
                queryset=Variant.objects
                .filter(is_active=True)
                .select_related('selector_value__type')
                .order_by('id')
            )
            total_inv_subq = (Variant.objects
                              .values('product_id')
                              .filter(product=OuterRef('id'), is_active=True)
                              .annotate(sum=Sum('inventory'))
                              .values('sum'))
            price_min_subq = (Variant.objects
                              .values('product_id')
                              .filter(product=OuterRef('id'), is_active=True)
                              .annotate(min=Min('price'))
                              .values('min'))
            return (Product.objects
                    .select_related('brand')
                    .select_related('category')
                    .prefetch_related(prefetch_variants)
                    .filter(is_active=True)
                    .annotate(total_inventory=Coalesce(Subquery(total_inv_subq), Value(0)))
                    .annotate(price_min=Coalesce(Subquery(price_min_subq), Value(0)))
                    .order_by('-created_at'))

        prefetch_attrs = Prefetch(
            'attribute_values',
            queryset=ProductAttributeValue.objects.select_related('attribute__unit')
        )
        prefetch_variants_detail = Prefetch(
            'variants',
            queryset=Variant.objects
            .filter(is_active=True)
            .select_related('selector_value__type')
            .select_related('product')
            .order_by('id')
        )
        return (Product.objects
                .select_related('brand')
                .select_related('category__selector_type')
                .prefetch_related(prefetch_variants_detail)
                .prefetch_related(prefetch_attrs)
                .filter(is_active=True)
                .order_by('-created_at'))

    @action(detail=False, methods=['GET'], url_path='get-price-range')
    def get_price_range(self, request):
        min_price_subq = (Variant.objects
                          .values('product_id')
                          .filter(product=OuterRef('id'))
                          .annotate(min=Min('price'))
                          .values('min'))
        max_price_subq = (Variant.objects
                          .values('product_id')
                          .filter(product=OuterRef('id'))
                          .annotate(max=Max('price'))
                          .values('max'))

        price_min = (Product.objects
                     .filter(is_active=True)
                     .annotate(price_min=Subquery(min_price_subq))
                     .aggregate(min=Min('price_min'))['min'] or 0)
        price_max = (Product.objects
                     .filter(is_active=True)
                     .annotate(price_max=Subquery(max_price_subq))
                     .aggregate(max=Max('price_max'))['max'] or 0)

        response = {
            'min': price_min,
            'max': price_max,
        }
        return Response(response)

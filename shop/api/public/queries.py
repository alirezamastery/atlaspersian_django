from django.db.models import *

from shop.models import *


__all__ = [
    'get_prefetch_variants',
    'get_total_inventory_subq',
    'get_price_min_subq',
]


def get_prefetch_variants():
    return Prefetch(
        'variants',
        queryset=Variant.objects
        .filter(is_active=True)
        .select_related('selector_value__type')
        .order_by('id')
    )


def get_total_inventory_subq():
    return (Variant.objects
            .values('product_id')
            .filter(product=OuterRef('id'), is_active=True)
            .annotate(sum=Sum('inventory'))
            .values('sum'))


def get_price_min_subq(*, filters: dict | None = None):
    if filters is None:
        filters = {}
    return (Variant.objects
            .values('product_id')
            .filter(product=OuterRef('id'), is_active=True, **filters)
            .annotate(min=Min('price'))
            .values('min'))

from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter
from django_filters.constants import EMPTY_VALUES

from shop.models import *


__all__ = [
    'ProductFilterPublic',
]


class CustomOrderingFilter(OrderingFilter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        val = value[0]
        if val == 'n':
            return qs.order_by('-has_inventory', '-created_at')
        elif val == 'p':
            return qs.order_by('-has_inventory', 'price_min')
        elif val == '-p':
            return qs.order_by('-has_inventory', '-price_min')
        elif val == 'l':
            return qs.order_by('-has_inventory', '-score')
        elif val == 'd':
            return qs.order_by('-has_inventory', '-max_discount')
        elif val == 's':
            return qs.order_by('-has_inventory', '-sale_sum')

        return qs


class ProductFilterPublic(filters.FilterSet):
    q = filters.CharFilter(method='search_in_fields')
    pmin = filters.NumberFilter(field_name='price_min', lookup_expr='gte')
    pmax = filters.NumberFilter(field_name='price_min', lookup_expr='lte')
    # pmin = filters.NumberFilter(method='price_min_filter')
    # pmax = filters.NumberFilter(method='price_max_filter')
    is_av = filters.BooleanFilter(method='is_available')
    cat_id = filters.NumberFilter(field_name='category_id')

    # map: newest price -price liked discount sale_count
    o = CustomOrderingFilter(fields=['n', 'p', '-p', 'l', 'd', 's'])

    class Meta:
        model = Product
        fields = ['q', 'pmax', 'pmin', 'is_av', 'cat_id']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title__icontains=value))

    def is_available(self, qs, name, value):
        if value:
            return qs.filter(total_inventory__gt=0)
        return qs

    def price_min_filter(self, qs, name, value):
        if value > -1:
            return qs.filter(price_min__gte=value)
        return qs

    def price_max_filter(self, qs, name, value):
        if value > -1:
            return qs.filter(price_min__lte=value)
        return qs

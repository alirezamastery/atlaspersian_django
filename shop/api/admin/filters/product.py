from django.db.models import Q
from django_filters import rest_framework as filters

from shop.models import *


__all__ = [
    'ProductFilterAdmin',
]


class ProductFilterAdmin(filters.FilterSet):
    q = filters.CharFilter(method='search_in_fields')

    class Meta:
        model = Product
        fields = ['q']

    def search_in_fields(self, qs, name, value):
        return qs.filter(Q(title__icontains=value) | Q(brand__title=value))

from django_filters import rest_framework as filters

from shop.models import *


__all__ = [
    'CategoryFilterAdmin',
]


class CategoryFilterAdmin(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['search']

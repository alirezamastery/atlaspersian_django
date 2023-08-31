from django_filters import rest_framework as filters

from shop.models import *


__all__ = [
    'AttributeFilterAdmin',
    'AttributeUnitFilterAdmin',
]


class AttributeFilterAdmin(filters.FilterSet):
    q = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Attribute
        fields = ['q']


class AttributeUnitFilterAdmin(filters.FilterSet):
    q = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = AttributeUnit
        fields = ['q']

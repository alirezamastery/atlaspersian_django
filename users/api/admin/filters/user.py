from django_filters import rest_framework as filters

from users.models import *


__all__ = [
    'UserFilterAdmin',
]


class UserFilterAdmin(filters.FilterSet):
    q = filters.CharFilter(field_name='mobile', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['q', 'is_active']

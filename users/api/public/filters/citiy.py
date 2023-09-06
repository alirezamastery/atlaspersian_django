from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters import OrderingFilter
from django_filters.constants import EMPTY_VALUES

from users.models import *


__all__ = [
    ''
]


class CityFilterPublic(filters.FilterSet):
    province = filters.NumberFilter(field_name='province_id')

    class Meta:
        model = City
        fields = ['province']

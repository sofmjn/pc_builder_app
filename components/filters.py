import django_filters
from django_filters import rest_framework as filters
from .models import Component

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ComponentFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    type = CharInFilter(field_name='type', lookup_expr='in')     # можно type=cpu&type=gpu
    brand = CharInFilter(field_name='brand', lookup_expr='in')    # можно brand=Intel&brand=NVIDIA

    class Meta:
        model = Component
        fields = ['type', 'brand', 'price_min', 'price_max']

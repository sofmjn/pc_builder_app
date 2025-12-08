import django_filters
from django_filters import rest_framework as filters
from .models import Component

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ComponentFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    type = CharInFilter(field_name='type', lookup_expr='in')
    vendor = CharInFilter(field_name='vendor', lookup_expr='in')

    class Meta:
        model = Component
        fields = ['type', 'vendor', 'price_min', 'price_max']


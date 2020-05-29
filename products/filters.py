from django_filters import rest_framework as filters

from .models import Product, Section


class ProductFilter(filters.FilterSet):
    section = filters.NumberFilter(method='filter_by_section')
    exclude = filters.BaseInFilter(method='filter_by_excluded')
    include_all = filters.BaseInFilter(method='filter_by_all_included')
    include_any = filters.BaseInFilter(method='filter_by_any_included')

    class Meta:
        model = Product
        fields = ['section' ,'exclude', 'include_all', 'include_any']
    
    def filter_by_section(self, queryset, name, value):
        sections_ids = Section.objects.get(pk=value).get_most_nested()
        return queryset.filter(section__in=sections_ids)

    def filter_by_excluded(self, queryset, name, value):
        return queryset.exclude_all(value)
    
    def filter_by_all_included(self, queryset, name, value):
        return queryset.include_all(value)
    
    def filter_by_any_included(self, queryset, name, value):
        return queryset.include_any(value)

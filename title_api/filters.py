from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from title_api.models import Title


class TitleFilter(FilterSet):
    """Title get params filtration"""
    category = CharFilter(field_name='category', lookup_expr='slug')
    genre = CharFilter(field_name='genre', lookup_expr='slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter()

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')

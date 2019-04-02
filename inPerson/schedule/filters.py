from .models import Section
import django_filters

class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = Section
        fields = ["code", "catalog_number", "title"]

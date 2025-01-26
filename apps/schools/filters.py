from django_filters.rest_framework import FilterSet
from .models import School


class SchoolFilter(FilterSet):
    class Meta:
        model = School
        fields = {
            "name": [
                "iexact",
                "icontains",
                "istartswith",
                "iendswith",
            ],
        }

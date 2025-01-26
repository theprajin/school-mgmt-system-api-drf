from django_filters.rest_framework import FilterSet
from .models import Student


class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            "first_name": [
                "iexact",
                "icontains",
                "istartswith",
                "iendswith",
            ],
            "last_name": [
                "iexact",
                "icontains",
                "istartswith",
                "iendswith",
            ],
        }

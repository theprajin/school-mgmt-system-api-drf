from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "age", "school")
    list_filter = ("first_name", "last_name", "age", "school", "created", "updated")
    list_per_page = 20
    ordering = ("first_name", "last_name", "age")
    search_fields = ("first_name__istartswith", "icontains")

    def get_queryset(self, request):
        # Use prefetch_related for reverse relationships
        return super().get_queryset(request).select_related("school")

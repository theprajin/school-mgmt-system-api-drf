from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "max_students", "current_students")
    list_filter = ("name", "max_students", "created", "updated")
    list_per_page = 20
    ordering = ("name",)
    search_fields = ("name__istartswith", "icontains")

    def get_queryset(self, request):
        # Use prefetch_related for reverse relationships
        return super().get_queryset(request).prefetch_related("students")

    def current_students(self, obj):
        return obj.students.count()

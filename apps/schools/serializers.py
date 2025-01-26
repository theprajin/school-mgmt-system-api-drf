from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    current_students = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ("id", "name", "max_students", "current_students")

    def get_current_students(self, obj):
        return obj.students.count()

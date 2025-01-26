from rest_framework import serializers
from .models import Student
from apps.schools.serializers import SchoolSerializer


class StudentSerializer(serializers.ModelSerializer):
    school_id = serializers.PrimaryKeyRelatedField(source="school", read_only=True)

    class Meta:
        model = Student
        fields = ("id", "first_name", "last_name", "age", "school_id")

    def validate_age(self, value):
        if not (5 <= value <= 120):
            raise serializers.ValidationError("Age must be between 5 and 120.")

        return value

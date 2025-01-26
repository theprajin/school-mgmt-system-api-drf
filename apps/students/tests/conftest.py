import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.schools.models import School
from apps.students.models import Student

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(role="admin"):
        user = User.objects.create_user(
            username=f"test_{role}",
            password="password123",
            role=role,
        )
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate


@pytest.fixture
def create_school(db):
    def do_create_school(**kwargs):
        # Set default values and allow overrides
        defaults = {"name": "Test School", "max_students": 10}
        defaults.update(kwargs)
        return School.objects.create(**defaults)

    return do_create_school


@pytest.fixture
def create_student(db):
    def do_create_student(school, **kwargs):
        # Set default values and allow overrides
        defaults = {"first_name": "John", "last_name": "Doe", "age": 15}
        defaults.update(kwargs)
        return Student.objects.create(school=school, **defaults)

    return do_create_student

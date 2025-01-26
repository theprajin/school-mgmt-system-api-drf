import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.schools.models import School

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_admin_user(db):
    def do_create_admin_user():
        return User.objects.create_user(
            username="admin", password="admin", role="admin"
        )

    return do_create_admin_user


@pytest.fixture
def create_staff_user(db):
    def do_create_staff_user():
        return User.objects.create_user(
            username="staff", password="staff", role="staff"
        )

    return do_create_staff_user


@pytest.fixture
def create_school(db):
    def do_create_school(name="Springfield High", max_students=500):
        return School.objects.create(name=name, max_students=max_students)

    return do_create_school


@pytest.fixture
def create_student(db):
    def do_create_student(school, first_name="John", last_name="Doe", age=15):
        return school.students.create(
            first_name=first_name, last_name=last_name, age=age
        )

    return do_create_student

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_authenticate


@pytest.fixture
def create_user(db):
    def do_create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return do_create_user


@pytest.fixture
def login_user(api_client):
    def do_login_user(credentials):
        return api_client.post("/api/auth/login/", credentials)

    return do_login_user


@pytest.fixture
def logout_user(api_client, authenticate):
    def do_logout_user(refresh_token):
        # Authenticate the user before making the request
        authenticate(is_staff=True)  # Assuming only staff users can log out
        return api_client.post("/api/auth/logout/", {"refresh": refresh_token})

    return do_logout_user

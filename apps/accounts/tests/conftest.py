from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client, create_user):
    def do_authenticate(is_staff=False, **user_data):
        # Create a user with the given data
        user = create_user(is_staff=is_staff, **user_data)
        # Force authentication
        api_client.force_authenticate(user=user)
        return user

    return do_authenticate


@pytest.fixture
def create_user(db):
    def do_create_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return do_create_user


@pytest.fixture
def login_user(api_client):
    def do_login_user(credentials):
        # Make sure the Content-Type header is set for login
        return api_client.post("/api/auth/login/", credentials, format="json")

    return do_login_user


@pytest.fixture
def logout_user(api_client):
    def do_logout_user(refresh_token):
        # Ensure the Content-Type header is set for logout
        return api_client.post(
            "/api/auth/logout/",
            {"refresh": refresh_token},
            format="json",
        )

    return do_logout_user

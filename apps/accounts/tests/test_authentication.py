from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import pytest


@pytest.mark.django_db
class TestAuthentication:
    def test_login_success(self, create_user, login_user):
        user = create_user(username="admin", password="admin", role="admin")
        response = login_user({"username": user.username, "password": "admin"})

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self, create_user, login_user):
        create_user(username="admin", password="admin", role="admin")
        response = login_user({"username": "admin", "password": "wrongpassword"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data

    def test_logout_success(self, create_user, login_user, logout_user):
        # Create and log in a user
        user = create_user(username="admin", password="admin", role="admin")
        login_response = login_user({"username": user.username, "password": "admin"})

        refresh_token = login_response.data["refresh"]

        # Log out and verify the response
        response = logout_user(refresh_token)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Logout successful."

        # Attempt to use the blacklisted refresh token
        from rest_framework_simplejwt.exceptions import TokenError

        with pytest.raises(TokenError):
            RefreshToken(refresh_token).check_blacklist()

    def test_logout_invalid_token(self, logout_user, authenticate):

        # Authenticate the user before calling the logout endpoint
        authenticate(is_staff=True)
        response = logout_user("invalidtoken")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Token is invalid or expired."

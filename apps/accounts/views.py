from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from .serializers import CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Obtain JWT tokens",
    description="Authenticate user and return access/refresh tokens",
    examples=[
        OpenApiExample(
            "Login Request Example",
            value={"username": "admin", "password": "admin"},
            request_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Login Response Example",
            value={
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            "Invalid Credentials Example",
            value={"detail": "No active account found with the given credentials"},
            response_only=True,
            status_codes=["401"],
        ),
    ],
    responses={
        200: CustomTokenObtainPairSerializer,
        401: OpenApiResponse(description="Invalid credentials"),
    },
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Logout user",
    description="Invalidate the refresh token to log out the user.",
    request={
        "type": OpenApiTypes.OBJECT,
        "properties": {
            "refresh": {
                "type": "string",
                "description": "The refresh token to invalidate.",
            }
        },
        "required": ["refresh"],
    },
    responses={
        200: {"description": "Logout successful."},
        400: {"description": "Invalid or missing token."},
    },
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Token is invalid or expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

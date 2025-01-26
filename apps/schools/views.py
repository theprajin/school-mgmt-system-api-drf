from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from .filters import SchoolFilter
from .models import School
from .serializers import SchoolSerializer
from .pagination import DefaultPagination
from apps.core.permissions import IsAdmin, IsStaffOrAdmin


@extend_schema_view(
    list=extend_schema(
        tags=["Schools"],
        summary="List all schools",
        description="Retrieve a list of all schools with optional filters and search capabilities. Supports filtering by name and max student capacity.",
        parameters=[
            OpenApiParameter(
                name="name",
                type=str,
                description="Filter schools by name",
                required=False,
            ),
            OpenApiParameter(
                name="max_students",
                type=int,
                description="Filter by maximum student capacity",
                required=False,
            ),
            OpenApiParameter(
                name="search",
                type=str,
                description="Search schools by name",
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                "Success Response",
                value={
                    "count": 2,
                    "next": None,
                    "previous": None,
                    "results": [
                        {"id": 1, "name": "Springfield High", "max_students": 500}
                    ],
                },
                response_only=True,
            )
        ],
    ),
    create=extend_schema(
        tags=["Schools"],
        summary="Create a new school",
        description="Add a new school by providing its name and maximum student capacity. Only admins are allowed to perform this action.",
        examples=[
            OpenApiExample(
                "Create School Request",
                value={"name": "New Academy", "max_students": 200},
                request_only=True,
            )
        ],
        responses={
            201: SchoolSerializer,
            403: OpenApiResponse(description="Admin access required"),
        },
    ),
    retrieve=extend_schema(
        tags=["Schools"],
        summary="Retrieve school details",
        description="Fetch details of a specific school by its ID. Returns the school's name and maximum student capacity.",
        responses={
            200: SchoolSerializer,
            404: OpenApiResponse(description="School not found"),
        },
    ),
    update=extend_schema(
        tags=["Schools"],
        summary="Update a school",
        description="Update the details of an existing school, such as its name or maximum student capacity. Only admins are allowed to perform this action.",
        examples=[
            OpenApiExample(
                "Update Request",
                value={"name": "Updated School Name", "max_students": 300},
            )
        ],
    ),
    destroy=extend_schema(
        tags=["Schools"],
        summary="Delete a school",
        description=(
            "Delete a school by its ID. Schools with enrolled students cannot be deleted. Only admins are allowed to perform this action."
        ),
        responses={
            204: OpenApiResponse(description="School deleted successfully"),
            400: OpenApiResponse(
                description="School has students",
                examples=[
                    OpenApiExample(
                        "Error Response",
                        value={"detail": "Cannot delete a school with students."},
                    )
                ],
            ),
            403: OpenApiResponse(description="Admin access required"),
        },
    ),
)
class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SchoolFilter
    pagination_class = DefaultPagination
    http_method_names = ["get", "post", "put", "delete"]
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [IsStaffOrAdmin()]

    def destroy(self, request, *args, **kwargs):
        school = get_object_or_404(School, id=kwargs["pk"])
        if school.students.exists():
            return Response(
                {"detail": "Cannot delete a school with students."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

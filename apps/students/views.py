from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from apps.schools.models import School
from .filters import StudentFilter
from .pagination import DefaultStudentPagination
from .models import Student
from .serializers import StudentSerializer
from apps.core.permissions import IsStaffOrAdmin


@extend_schema_view(
    list=extend_schema(
        tags=["Students"],
        summary="List all students in a school",
        description=(
            "Retrieve a paginated list of all students associated with a specific school. "
            "You can filter students by their age or order them by ID, first name, or last name."
        ),
        parameters=[
            OpenApiParameter(
                name="school_pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="School ID to filter students",
            ),
            OpenApiParameter(
                name="age",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter students by exact age",
            ),
            OpenApiParameter(
                name="ordering",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Order students by field (id, first_name, last_name)",
            ),
        ],
        examples=[
            OpenApiExample(
                "Success Example",
                value={
                    "count": 2,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "first_name": "John",
                            "last_name": "Doe",
                            "age": 15,
                            "school": 1,
                        }
                    ],
                },
                response_only=True,
                status_codes=["200"],
            )
        ],
    ),
    create=extend_schema(
        tags=["Students"],
        summary="Create a student in a school",
        description=(
            "Add a new student to a specific school by providing their details "
            "(first name, last name, and age). The school must have available capacity."
        ),
        parameters=[
            OpenApiParameter(
                name="school_pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="School ID to create student in",
            )
        ],
        examples=[
            OpenApiExample(
                "Create Student Request",
                value={"first_name": "Jane", "last_name": "Smith", "age": 16},
                request_only=True,
            ),
            OpenApiExample(
                "Capacity Error Response",
                value={"detail": "School has reached maximum capacity"},
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
)
class NestedStudentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StudentSerializer
    permission_classes = [IsStaffOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = StudentFilter
    pagination_class = DefaultStudentPagination
    ordering_fields = ["id", "first_name", "last_name"]
    search_fields = ["first_name", "last_name"]

    def get_queryset(self):
        """
        Filter students by the school ID from the path.
        """
        return Student.objects.filter(school_id=self.kwargs["school_pk"])

    def perform_create(self, serializer):
        """
        Create a new student while ensuring the school has not exceeded its maximum capacity.
        """
        school = School.objects.get(pk=self.kwargs["school_pk"])
        if school.students.count() >= school.max_students:
            raise ValidationError("School has reached maximum capacity")
        serializer.save(school=school)


@extend_schema_view(
    retrieve=extend_schema(
        tags=["Students"],
        summary="Retrieve a student's details",
        description="Fetch the details of a specific student by their ID.",
        responses={
            200: StudentSerializer,
            404: OpenApiResponse(description="Student not found"),
        },
    ),
    update=extend_schema(
        tags=["Students"],
        summary="Update a student's details",
        description="Update all the details of a specific student by providing their full details.",
        examples=[
            OpenApiExample(
                "Update Request",
                value={"first_name": "John", "last_name": "Smith", "age": 16},
                request_only=True,
            )
        ],
    ),
    partial_update=extend_schema(
        tags=["Students"],
        summary="Partially update a student's details",
        description=(
            "Update specific fields of a student's details, such as their age or last name."
        ),
        examples=[
            OpenApiExample(
                "Partial Update Request",
                value={"age": 16},
                request_only=True,
            )
        ],
    ),
    destroy=extend_schema(
        tags=["Students"],
        summary="Delete a student",
        description="Delete a specific student by their ID.",
        responses={
            204: OpenApiResponse(description="Student deleted successfully"),
            403: OpenApiResponse(description="Permission denied"),
        },
    ),
)
class StudentDetailViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStaffOrAdmin]

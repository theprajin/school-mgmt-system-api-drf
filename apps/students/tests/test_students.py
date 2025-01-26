import pytest
from rest_framework import status


@pytest.mark.django_db
class TestStudentViewSet:
    def test_create_student_success(self, api_client, authenticate, create_school):
        school = create_school()
        authenticate(role="admin")
        response = api_client.post(
            f"/api/schools/{school.id}/students/",
            {"first_name": "John", "last_name": "Doe", "age": 15},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["first_name"] == "John"

        def test_create_student_max_capacity(
            self, api_client, authenticate, create_school
        ):
            school = create_school(max_students=1)
            authenticate(role="admin")

            # Create the first student to fill the capacity
            response1 = api_client.post(
                f"/api/schools/{school.id}/students/",
                {"first_name": "John", "last_name": "Doe", "age": 15},
            )
            assert response1.status_code == status.HTTP_201_CREATED

            # Try adding another student
            response2 = api_client.post(
                f"/api/schools/{school.id}/students/",
                {"first_name": "Jane", "last_name": "Smith", "age": 16},
            )

            assert response2.status_code == status.HTTP_400_BAD_REQUEST
            assert response2.data["detail"] == "School has reached maximum capacity."

    def test_list_students_in_school(
        self, api_client, authenticate, create_school, create_student
    ):
        school = create_school()
        authenticate(role="staff")
        create_student(school=school, first_name="John", last_name="Doe", age=15)

        response = api_client.get(f"/api/schools/{school.id}/students/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

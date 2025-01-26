import pytest
from rest_framework import status


@pytest.mark.django_db
class TestSchoolViewSet:
    def test_create_school_as_admin(self, api_client, create_admin_user):

        admin = create_admin_user()
        school_data = {"name": "Springfield High", "max_students": 500}
        list_url = "/api/schools/"

        api_client.force_authenticate(user=admin)
        response = api_client.post(list_url, school_data)

        print(response.status_code, response.data)  # Debugging
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == school_data["name"]

    def test_delete_school_with_students(
        self, api_client, create_admin_user, create_school, create_student
    ):

        admin = create_admin_user()
        school = create_school()
        create_student(school)

        delete_url = f"/api/schools/{school.id}/"
        api_client.force_authenticate(user=admin)
        response = api_client.delete(delete_url)

        print(response.status_code, response.data)  # Debugging
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Cannot delete a school with students."

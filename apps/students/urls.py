# from rest_framework.routers import DefaultRouter
# from rest_framework_nested.routers import NestedDefaultRouter
# from apps.schools.urls import router
# from .views import StudentViewSet


# schools_router = NestedDefaultRouter(router, r"schools", lookup="school")
# schools_router.register(r"students", StudentViewSet, basename="school-students")

# student_router = DefaultRouter()
# student_router.register(r"students", StudentViewSet, basename="students")

# urlpatterns = schools_router.urls + student_router.urls


from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from apps.schools.urls import router as schools_router
from .views import NestedStudentViewSet, StudentDetailViewSet

# Nested routes (only list/create)
students_router = routers.NestedSimpleRouter(
    schools_router, r"schools", lookup="school"
)
students_router.register(r"students", NestedStudentViewSet, basename="school-students")

# Standalone routes (retrieve/update/delete)
student_router = DefaultRouter()
student_router.register(r"students", StudentDetailViewSet, basename="students")

urlpatterns = students_router.urls + student_router.urls

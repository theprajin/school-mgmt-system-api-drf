from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet

app_name = "schools"


router = DefaultRouter()
router.register(r"schools", SchoolViewSet, basename="schools")

urlpatterns = router.urls

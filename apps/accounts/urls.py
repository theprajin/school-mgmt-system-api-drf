from django.urls import path
from .views import CustomTokenObtainPairView, LogoutView

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

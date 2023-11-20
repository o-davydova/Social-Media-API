from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CreateUserView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
]

app_name = "user"

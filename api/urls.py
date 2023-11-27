from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("user/", include("user.urls", namespace="user")),
    path(
        "user_profile/",
        include("user_profile.urls", namespace="user-profile"),
    ),
    path(
        "post/",
        include("post.urls", namespace="post"),
    ),
    path("doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    path(
        "doc/redoc/",
        SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
]

app_name = "api"

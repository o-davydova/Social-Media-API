from django.urls import path, include

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
]

app_name = "api"

from rest_framework import routers

from user_profile.views import UserProfileViewSet

router = routers.DefaultRouter()
router.register("user_profiles", UserProfileViewSet)

urlpatterns = router.urls

app_name = "user-profile"

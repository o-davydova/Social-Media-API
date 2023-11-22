from django.contrib import admin

from user.admin import WhoDidItAdmin
from user_profile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(WhoDidItAdmin):
    list_display = ("created_by", "bio", "created_at", "updated_at")
    search_fields = ("created_by__email",)
    ordering = ("created_by", "-updated_at",)

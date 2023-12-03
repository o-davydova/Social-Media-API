from rest_framework.permissions import SAFE_METHODS, BasePermission


class CanModifyOwnObjectOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in ("PUT", "PATCH", "DELETE")
            and obj.created_by == request.user
        )

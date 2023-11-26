from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import CanModifyOwnObjectOnly
from user.views import WhoDidItMixin
from user_profile.models import UserProfile, UserProfileFollow
from user_profile.serializers import (
    UserProfileImageSerializer,
    UserProfileListSerializer,
    UserProfileSerializer,
    UserProfileDetailSerializer,
    UserProfileFollowSerializer,
)


class UserProfileViewSet(WhoDidItMixin, viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [
        CanModifyOwnObjectOnly,
    ]

    def get_queryset(self):
        queryset = self.queryset.annotate(
            followers_count=(Count("followers")),
            following_count=(Count("following")),
            posts_count=(Count("posts")),
        )

        if self.action != "create":
            queryset.select_related("followers", "following").prefetch_related(
                "posts"
            )

        for param_name in ["email", "first_name", "last_name", "username"]:
            param = self.request.query_params.get(param_name)

            if param:
                queryset = queryset.filter(
                    **{f"created_by__{param_name}__icontains": param}
                )

        created_by = self.request.query_params.get("user_id")
        if created_by:
            queryset = queryset.filter(created_by=created_by)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return UserProfileListSerializer

        if self.action == "retrieve":
            return UserProfileDetailSerializer

        if self.action == "upload_image":
            return UserProfileImageSerializer

        if self.action in ["follow", "unfollow"]:
            return UserProfileFollowSerializer

        return UserProfileSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific user profile"""
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="follow",
    )
    def follow(self, request, pk=None):
        """Endpoint for following a specific user profile"""
        follower = UserProfile.objects.get(created_by=self.request.user)
        followed = self.get_object()

        serializer = UserProfileFollowSerializer(
            data={
                "following": followed.pk,
                "follower": follower.pk,
            },
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unfollow",
    )
    def unfollow(self, request, pk=None):
        """Endpoint for unfollowing a specific user profile"""
        follower = UserProfile.objects.get(created_by=self.request.user)
        followed = self.get_object()

        follow_instance = UserProfileFollow.objects.filter(
            follower=follower,
            following=followed,
        ).first()

        if follow_instance:
            follow_instance.delete()
            return Response(
                {"message": "Unfollowed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"message": "Not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

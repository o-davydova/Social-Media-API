import pytz
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db.models import Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from api.permissions import CanModifyOwnObjectOnly
from post.tasks import post_schedule_create
from user.views import WhoDidItMixin
from user_profile.models import UserProfile
from post.models import HashTag, Like, Comment, Post
from post.serializers import (
    HashTagSerializer,
    LikeSerializer,
    CommentSerializer,
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostImageSerializer,
)


class HashTagViewSet(viewsets.ModelViewSet):
    queryset = HashTag.objects.all()
    serializer_class = HashTagSerializer


class LikeViewSet(WhoDidItMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        CanModifyOwnObjectOnly,
    ]


class CommentViewSet(WhoDidItMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        CanModifyOwnObjectOnly,
    ]


class PostPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 100


class PostViewSet(WhoDidItMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        CanModifyOwnObjectOnly,
    ]

    def get_queryset(self):
        queryset = self.queryset.annotate(
            likes_count=(Count("likes", distinct=True)),
            comments_count=(Count("comments", distinct=True)),
        )

        if self.action != "create":
            queryset.select_related("likes", "comments").prefetch_related(
                "hashtags"
            )

        for param_name in ["email", "first_name", "last_name", "username"]:
            param = self.request.query_params.get(param_name)

            if param:
                queryset = queryset.filter(
                    **{f"created_by__{param_name}__icontains": param}
                )

        hashtags = self.request.query_params.get("hashtags")
        title = self.request.query_params.get("title")
        profile = self.request.query_params.get("profile")

        if hashtags:
            hashtags_ids = [int(str_id) for str_id in hashtags.split(",")]
            queryset = queryset.filter(hashtags__id__in=hashtags_ids)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if profile:
            queryset = queryset.filter(profile=profile)

        return queryset

    def get_serializer_class(self):
        if self.action in ["liked_posts", "list"]:
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        if self.action == "upload_image":
            return PostImageSerializer

        if self.action == "add_comment":
            return CommentSerializer

        if self.action in ["like", "remove_like"]:
            return LikeSerializer

        return PostSerializer

    def perform_create(self, serializer, *args, **kwargs):
        user_profile = UserProfile.objects.get(
            created_by_id=self.request.user.pk
        )
        post = super().perform_create(serializer, profile=user_profile)

        scheduled_time = post.scheduled_time

        if scheduled_time:
            timezone = pytz.timezone("Europe/Kiev")
            now = datetime.now().astimezone(timezone)

            if scheduled_time < now:
                raise ValidationError("Incorrect scheduled time.")

            if post.is_visible:
                raise ValidationError(
                    "Scheduled time is not applicable if post is visible."
                )

            post_schedule_create.apply_async(args=[post.id], eta=scheduled_time)

    def _create_interaction(self, request):
        post = self.get_object()
        data = request.data.copy()
        data["post"] = post.pk

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific user profile"""
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
    )
    def like(self, request, pk=None):
        """Endpoint for liking a specific user post"""
        return self._create_interaction(request)

    @action(
        methods=["POST"],
        detail=True,
        url_path="remove-like",
    )
    def remove_like(self, request, pk=None):
        """Endpoint for removing a like on specific user post"""
        created_by = self.request.user
        post = self.get_object()

        like_instance = Like.objects.filter(
            post=post,
            created_by=created_by,
        ).first()

        if like_instance:
            like_instance.delete()
            return Response(
                {"message": "Like removed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"message": "Post was not liked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        methods=["POST"],
        detail=True,
        url_path="add-comment",
    )
    def add_comment(self, request, pk=None):
        """Endpoint for commenting a specific user post"""
        return self._create_interaction(request)

    @action(
        methods=["GET"],
        detail=False,
        url_path="liked-posts",
    )
    def liked_posts(self, request):
        """Endpoint to retrieve the list of posts liked by the authenticated user."""
        liked_posts = self.get_queryset().filter(likes__created_by=request.user)
        serializer = self.get_serializer(liked_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                description="Filter by email (ex. ?email=example@gmail.com)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="first_name",
                description="Filter by first name (ex. ?first_name=John)",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="last_name",
                description="Filter by last name (ex. ?last_name=Smith)",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="username",
                description="Filter by username (ex. ?username=mate)",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="title",
                description="Filter by title (ex. ?title=Develop)",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="profile",
                description="Filter by profile id (ex. ?profile=2)",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="hashtags",
                description="Filter by hashtag ids (ex. ?hashtags=1,2)",
                type={"type": "list", "items": {"type": "number"}},
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

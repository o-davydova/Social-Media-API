from rest_framework import serializers

from post.models import HashTag, Like, Comment, Post
from user.serializers import WhoDidItSerializer


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ("id", "name")


class LikeSerializer(WhoDidItSerializer, serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "post", "created_by")


class CommentSerializer(WhoDidItSerializer, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "content") + WhoDidItSerializer.Meta.fields


class CommentListSerializer(WhoDidItSerializer, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content") + WhoDidItSerializer.Meta.fields


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "image")


class PostSerializer(WhoDidItSerializer, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "hashtags",
            "content",
            "image",
            "profile",
            "is_visible",
            "scheduled_time",
        ) + WhoDidItSerializer.Meta.fields

        read_only_fields = ("profile",)


class PostListSerializer(PostSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + (
            "likes_count",
            "comments_count",
        )


class PostDetailSerializer(PostSerializer):
    likes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="created_by_id"
    )
    comments = serializers.StringRelatedField(many=True, read_only=True)
    hashtags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + (
            "likes",
            "comments",
        )

from rest_framework import serializers

from user.serializers import WhoDidItSerializer
from user_profile.models import UserProfile, UserProfileFollow


class UserProfileFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileFollow
        fields = ("id", "follower", "following")


class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "image")


class UserProfileSerializer(WhoDidItSerializer, serializers.ModelSerializer):
    followers = UserProfileFollowSerializer(many=True, read_only=True)
    following = UserProfileFollowSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "bio",
            "image",
            "followers",
            "following",
        ) + WhoDidItSerializer.Meta.fields


class UserProfileListSerializer(UserProfileSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "bio",
            "image",
            "followers_count",
            "following_count",
            "posts_count",
        ) + WhoDidItSerializer.Meta.fields


class UserProfileDetailSerializer(UserProfileSerializer):
    followers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="follower_id"
    )
    following = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="following_id"
    )
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = UserProfileSerializer.Meta.fields + (
            "followers",
            "following",
            "posts",
        )

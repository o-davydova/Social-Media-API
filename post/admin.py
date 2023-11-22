from django.contrib import admin

from post.models import HashTag, Post, Like, Comment
from user.admin import WhoDidItAdmin

admin.site.register(HashTag)
admin.site.register(Like)


@admin.register(Post)
class PostAdmin(WhoDidItAdmin):
    list_display = ("title", "created_by", "created_at", "updated_at")
    search_fields = ("title", "created_by__email",)
    ordering = ("created_by", "-updated_at",)


@admin.register(Comment)
class CommentAdmin(WhoDidItAdmin):
    list_display = ("post", "content", "created_by", "created_at", "updated_at")
    search_fields = ("created_by__email",)
    ordering = ("post", "-updated_at",)

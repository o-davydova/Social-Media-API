import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from user.models import WhoDidIt
from user_profile.models import UserProfile


def get_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    dirname = f"{slugify(type(instance).__name__)}s/"

    return os.path.join("uploads/", dirname, filename)


class HashTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(WhoDidIt):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(null=True, upload_to=get_image_file_path)
    hashtags = models.ManyToManyField(HashTag, related_name="post", blank=True)
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="post",
    )

    def __str__(self):
        return f"{self.created_by}"


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )

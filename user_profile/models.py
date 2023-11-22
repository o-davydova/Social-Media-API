import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from user.models import WhoDidIt


def get_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    dirname = f"{slugify(type(instance).__name__)}s/"

    return os.path.join("uploads/", dirname, filename)


class UserProfile(WhoDidIt):
    bio = models.TextField()
    followers = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles_followers",
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles_following",
    )
    image = models.ImageField(null=True, upload_to=get_image_file_path)

    def __str__(self):
        return f"{self.created_by}"

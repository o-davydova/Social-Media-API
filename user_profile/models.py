import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from user.models import WhoDidIt


def get_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.created_by)}-{uuid.uuid4()}{extension}"
    dirname = f"{slugify(type(instance).__name__)}s"

    return os.path.join("uploads/", dirname, filename)


class UserProfile(WhoDidIt):
    bio = models.TextField()
    image = models.ImageField(
        blank=True, null=True, upload_to=get_image_file_path
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["created_by"], name="unique_created_by"
            )
        ]

    def __str__(self):
        return f"{self.id}: {self.created_by}"


class UserProfileFollow(models.Model):
    follower = models.ForeignKey(
        UserProfile,
        related_name="following",
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        UserProfile,
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_followers"
            )
        ]

    def validate_following(self):
        if self.follower == self.following:
            raise ValidationError("Cannot follow/unfollow your own profile.")

    def save(self, *args, **kwargs):
        self.validate_following()
        super(UserProfileFollow, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

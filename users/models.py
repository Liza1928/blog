from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


def upload_to_images(instance, filename):
    return f'user_images/{instance.id}/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=32, unique=True)
    image = models.ImageField(  # noqa: DJ01
        upload_to=upload_to_images, max_length=1024, null=True, blank=True
    )
    is_author = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "name"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "user"
        verbose_name_plural = (
            "users",
        )

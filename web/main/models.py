from typing import TypeVar

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')

def avatar_upload_path(obj: UserType, file_name: str):
    return f'avatars/{obj.id}/{file_name}'

class Gender(models.IntegerChoices):
    NOT_KNOWN = 0
    MALE = 1
    FEMALE = 2

class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    avatar = models.ImageField(blank=True, upload_to=avatar_upload_path, default='no-avatar.png')
    birthday = models.DateField(null=True, blank=True)
    gender = models.SmallIntegerField(choices=Gender.choices, default=Gender.NOT_KNOWN)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    @property
    def confirmation_key(self) -> str:
        return signing.dumps(obj=self.pk)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Permissions:

    values = (
        ('read', 'read'),
        ('write', 'write'),
        ('del', 'del'),
    )


class UserProfile(AbstractBaseUser):

    email = models.EmailField('email', unique=True)
    is_active = models.BooleanField('active', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

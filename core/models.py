from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, name, password, *args, **kwargs):
        user = self.model(name=name)
        user.is_active = True
        user.is_superuser = False
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, password, *args, **kwargs):
        user = self.model(name=name)
        user.is_active = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):

    name = models.CharField('user name', max_length=50, unique=True)
    is_active = models.BooleanField('active', default=False)
    is_superuser = models.BooleanField('superuser', default=False)

    objects = UserManager()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def has_permission(self, permission):
        if Permission.objects.filter(user=self, status=permission).count() > 0:
            return True
        return False


class Permission(models.Model):

    class Choices:
        watch_list = 'watch_list'
        create_user = 'create user'
        edit_user = 'edit user'
        del_user = 'del user'

        values = (
            (watch_list, 'watch_list'),
            (create_user, 'create user'),
            (edit_user, 'edit user'),
            (del_user, 'del user'),
        )

    user = models.ForeignKey(User, verbose_name='User')
    status = models.CharField('status', max_length=15, choices=Choices.values)

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'

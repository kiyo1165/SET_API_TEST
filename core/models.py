from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is must')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # UserManagerをインスタンス化
    objects = UserManager()

    # デフォルトの認証をEmailにする。（変更前はusernameになっている。）
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name


class Profile(models.Model):
    nickname = models.CharField(max_length=20)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

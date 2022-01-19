from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    email = models.CharField(max_length=200, verbose_name='メールアドレス')
    username = models.CharField(max_length=30, unique=True, verbose_name='ユーザー名')
    password1 = models.CharField(max_length=20, verbose_name='パスワード')
    password2 = models.CharField(max_length=20, verbose_name='パスワードの再入力')

    def __str__(self):
        return self.username

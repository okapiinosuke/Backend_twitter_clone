from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(AbstractUser):
    email = models.EmailField(
        _('email'), 
        max_length=200
    )
    username = models.CharField(
        _('username'), 
        max_length=30, 
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    password = models.CharField(
        _('password'), 
        max_length=20
    )

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        Account, 
        on_delete=models.CASCADE,
        related_name = 'profile'
    )

    profile = models.TextField(
        _('profile'),
        default = ""
    ) 

    def __str__(self):
        return self.profile


class Tweet(models.Model):
    user = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE,
        related_name='tweet'
        )
    content = models.CharField(
        _('content'), 
        max_length=255
    )
    created_at = models.DateTimeField(
        verbose_name="投稿日時",
        auto_now_add=True
    )
    
    def __str__(self):
        return self.content

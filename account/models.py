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
    profile = models.TextField(
        _('profile')
    )

    def __str__(self):
        return self.username

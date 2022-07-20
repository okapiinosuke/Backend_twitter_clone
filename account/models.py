from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(AbstractUser):
    email = models.EmailField(_("email"), max_length=200)
    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    password = models.CharField(_("password"), max_length=20)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="profile"
    )
    profile = models.TextField(_("profile"), default="")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return self.profile


class FollowConnection(models.Model):
    follower = models.ForeignKey(
        Account, related_name="follower", on_delete=models.CASCADE
    )
    followee = models.ForeignKey(
        Account, related_name="followee", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followee"], name="follow_connection_unique"
            ),
        ]

    def __str__(self):
        return f"{self.follower.username} : {self.followee.username}"

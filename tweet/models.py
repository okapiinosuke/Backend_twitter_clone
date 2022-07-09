from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account


class Tweet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="tweet")
    content = models.CharField(_("content"), max_length=255)
    created_at = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)

    def __str__(self):
        return self.content

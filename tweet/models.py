from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import Account


class Tweet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="tweet")
    content = models.CharField(_("content"), max_length=255)
    created_at = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)

    def __str__(self):
        return self.content


class FavoriteConnection(models.Model):
    favorite_account = models.ForeignKey(
        Account, related_name="favorite_account", on_delete=models.CASCADE
    )
    favorited_tweet = models.ForeignKey(
        Tweet, related_name="favorited_tweet", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["favorite_account", "favorited_tweet"],
                name="favorite_connection_unique",
            ),
        ]

    def __str__(self):
        return f"{self.favorite_account.username} : {self.favorited_tweet.content}"

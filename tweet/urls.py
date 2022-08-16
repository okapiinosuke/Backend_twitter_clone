from django.urls import path

from . import views

app_name = "tweet"


urlpatterns = [
    path("tweets/<int:tweet_id>", views.tweet_detail_view, name="tweet_detail"),
    path("tweets/<int:tweet_id>/delete", views.delete_tweet_view, name="delete_tweet"),
    path(
        "tweets/<int:tweet_id>/favorite",
        views.favorite_tweet_view,
        name="favorite_tweet",
    ),
    path(
        "tweets/<int:tweet_id>/unfavorite",
        views.unfavorite_tweet_view,
        name="unfavorite_tweet",
    ),
]

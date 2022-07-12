from django.urls import path

from . import views

app_name = "tweet"


urlpatterns = [
    path("tweets/<int:tweet_id>", views.tweet_detail_view, name="tweet_detail"),
    path("tweets/<int:tweet_id>/delete", views.delete_tweet_view, name="delete_tweet"),
]

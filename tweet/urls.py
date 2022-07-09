from django.urls import path

from . import views

app_name = "tweet"


urlpatterns = [
    path("tweet_<int:tweet_id>", views.tweet_detail_view, name="tweet_detail"),
    path("tweet_{<int:tweet_id>}/delete", views.delete_tweet_view, name="delete_tweet"),
]

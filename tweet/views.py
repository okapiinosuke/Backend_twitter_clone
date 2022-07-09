from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .models import Tweet


@login_required
def tweet_detail_view(request, tweet_id):
    """
    ツイートの詳細を編集するページ
    """

    if request.method == "GET":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        return render(request, "tweet/tweet_detail.html", {"tweet": tweet})
    return HttpResponseNotAllowed(["GET"])


@login_required
def delete_tweet_view(request, tweet_id):
    """
    ツイートを削除するページ
    """

    if request.method == "GET":
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        if tweet.user == request.user:
            tweet.delete()
            return redirect("/home/")
        else:
            raise PermissionDenied
    return HttpResponseNotAllowed(["GET"])

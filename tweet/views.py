from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Tweet


@login_required
@require_http_methods(["GET"])
def tweet_detail_view(request, tweet_id):
    """
    ツイートの詳細を編集するページ
    """

    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, "tweet/tweet_detail.html", {"tweet": tweet})


@login_required
@require_http_methods(["GET"])
def delete_tweet_view(request, tweet_id):
    """
    ツイートを削除するページ
    """

    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.user == request.user:
        tweet.delete()
        return redirect("/home/")
    else:
        raise PermissionDenied

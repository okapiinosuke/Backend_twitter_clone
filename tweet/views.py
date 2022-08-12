from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Tweet, FavoriteConnection


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


@login_required
@require_http_methods(["GET", "POST"])
def favorite_tweet_view(request, tweet_id):
    """
    ツイートをいいねするページ
    """

    if request.method == "POST":
        favorite_account = request.user
        favorited_tweet = Tweet.objects.filter(pk=tweet_id).first()
        if not favorited_tweet:
            return JsonResponse({"tweet_id": -1})

        _, is_created = FavoriteConnection.objects.get_or_create(
            favorite_account=favorite_account, favorited_tweet=favorited_tweet
        )
        if not is_created:
            return JsonResponse({"tweet_id": -1})
        return JsonResponse({"tweet_id": tweet_id})


@login_required
@require_http_methods(["GET", "POST"])
def unfavorite_tweet_view(request, tweet_id):
    """
    ツイートのいいねを解除するページ
    """

    if request.method == "POST":
        favorite_account = request.user
        favorited_tweet = Tweet.objects.filter(pk=tweet_id).first()
        if not favorited_tweet:
            return JsonResponse({"tweet_id": -1})

        favorite_connection = FavoriteConnection.objects.filter(
            favorite_account=favorite_account,
            favorited_tweet=favorited_tweet,
        ).first()
        if not favorite_connection:
            return JsonResponse({"tweet_id": -1})
        favorite_connection.delete()
        return JsonResponse({"tweet_id": tweet_id})

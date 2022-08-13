from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm, LoginForm, ProfileForm
from .models import Account, Profile, FollowConnection
from tweet.forms import TweetForm
from tweet.models import Tweet, FavoriteConnection


def start_view(request):
    """
    最初にアクセスした際に見れるページ
    """

    return render(request, "account/start.html")


def register_view(request):
    """
    ユーザ登録をする際にアクセスするページ
    """

    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            profile = Profile(
                user=Account.objects.get(username=form.cleaned_data["username"])
            )
            profile.save()
            return redirect(reverse("account:complete"))

    return render(request, "account/register.html", {"form": form})


def complete_view(request):
    """
    ユーザ登録が完了した際に見れるページ
    """

    return render(request, "account/complete.html")


def login_view(request):
    """
    ログインをする際に見れるページ
    """

    if request.method == "GET":
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("/home/")
        return render(request, "account/login.html", {"form": form})
    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def home_view(request):
    """
    ログイン後に遷移するページ（遷移確認のために仮で作成）
    """

    if request.method == "GET":
        user_profile = Profile.objects.get(user=request.user)
        form = TweetForm()
        tweet_list = Tweet.objects.all().order_by("-id")
        favorited_tweet_id_list = request.user.favorite_account.values_list(
            "favorited_tweet_id", flat=True
        )
        return render(
            request,
            "account/home.html",
            {
                "profile": user_profile,
                "form": form,
                "tweet_list": tweet_list,
                "favorited_tweet_id_list": favorited_tweet_id_list,
            },
        )
    elif request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        form = TweetForm(data=request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
        return redirect(reverse("account:home"))

    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def logout_view(request):
    """
    ログアウト後に遷移するページ（ログインページへ戻る）
    """

    logout(request)
    form = LoginForm()
    redirect_url = reverse("account:login")
    parameters = urlencode({"form": form})
    url = f"{redirect_url}?{parameters}"

    return redirect(url)


@login_required
def edit_profile_view(request):
    """
    プロフィールを編集するページ
    """

    if request.method == "GET":
        form = ProfileForm()
        user_profile = Profile.objects.get(user=request.user)
        return render(
            request,
            "account/edit_profile.html",
            {"form": form, "profile": user_profile},
        )
    elif request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        form = ProfileForm(data=request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
        return render(
            request,
            "account/edit_profile.html",
            {"form": form, "profile": user_profile},
        )
    return HttpResponseNotAllowed(["GET", "POST"])


@login_required
@require_http_methods(["GET"])
def account_detail_view(request, account_id):
    """
    アカウントの詳細を確認するページ
    """

    if request.method == "GET":
        account = get_object_or_404(
            Account.objects.select_related("profile"), pk=account_id
        )
        tweet_list = (
            Tweet.objects.select_related("user")
            .filter(user=account)
            .order_by("-created_at")
        )
        favorite_connection_list = (
            FavoriteConnection.objects.select_related("favorited_tweet")
            .filter(favorite_account=account)
            .order_by("-id")
        )
        is_follow = FollowConnection.objects.filter(
            follower=request.user, followee=account
        ).exists()
        followee_num = FollowConnection.objects.filter(follower=account).count()
        follower_num = FollowConnection.objects.filter(followee=account).count()
        return render(
            request,
            "account/account_detail.html",
            {
                "account": account,
                "profile": account.profile,
                "tweet_list": tweet_list,
                "is_follow": is_follow,
                "followee_num": followee_num,
                "follower_num": follower_num,
                "favorite_connection_list": favorite_connection_list,
            },
        )
    else:
        return HttpResponseBadRequest


@login_required
@require_http_methods(["GET"])
def account_followings_view(request, account_id):
    """
    アカウントがフォローしているアカウントの一覧を表示するページ
    """

    if request.method == "GET":
        account = get_object_or_404(
            Account.objects.select_related("profile"), pk=account_id
        )
        followee_connection_list = (
            FollowConnection.objects.select_related("followee")
            .filter(follower=account)
            .order_by("-id")
        )

        return render(
            request,
            "account/account_followings.html",
            {"followee_connection_list": followee_connection_list},
        )


@login_required
@require_http_methods(["GET"])
def account_followers_view(request, account_id):
    """
    アカウントがフォローされているアカウントの一覧を表示するページ
    """

    if request.method == "GET":
        account = get_object_or_404(
            Account.objects.select_related("profile"), pk=account_id
        )
        follower_connection_list = (
            FollowConnection.objects.select_related("follower")
            .filter(followee=account)
            .order_by("-id")
        )

        return render(
            request,
            "account/account_followers.html",
            {"follower_connection_list": follower_connection_list},
        )


@login_required
@require_http_methods(["GET", "POST"])
def follow_account_view(request, account_id):
    """
    アカウントをフォローするページ
    """

    if request.method == "POST":
        follower = request.user
        followee = get_object_or_404(Account, pk=account_id)

        if follower == followee:
            return HttpResponseForbidden()

        _, is_created = FollowConnection.objects.get_or_create(
            follower=follower, followee=followee
        )
        if not is_created:
            return HttpResponseForbidden()

    return redirect(reverse("account:account_detail", args=[account_id]))


@login_required
@require_http_methods(["GET", "POST"])
def unfollow_account_view(request, account_id):
    """
    アカウントをフォロー解除するページ
    """

    if request.method == "POST":
        follower = request.user
        followee = get_object_or_404(Account, pk=account_id)

        if follower == followee:
            return HttpResponseForbidden()
        follow = get_object_or_404(
            FollowConnection, follower=follower, followee=followee
        )
        follow.delete()

    return redirect(reverse("account:account_detail", args=[account_id]))

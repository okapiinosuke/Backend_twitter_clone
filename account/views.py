from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm, LoginForm, ProfileForm
from .models import Account, Profile, FollowConnection
from tweet.forms import TweetForm
from tweet.models import Tweet


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
        tweet_list = Tweet.objects.none()
        for tweet_each_user in Account.objects.prefetch_related("tweet"):
            tweet_list = tweet_list | tweet_each_user.tweet.all()
        tweet_list = tweet_list.order_by("-id")
        return render(
            request,
            "account/home.html",
            {"profile": user_profile, "form": form, "tweet_list": tweet_list},
        )
    elif request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        form = TweetForm(data=request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            form = TweetForm()
        return redirect("/home/")
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
        account = get_object_or_404(Account, pk=account_id)
        user_profile = Profile.objects.get(user=account)
        tweet_list = (
            (
                Account.objects.filter(pk=account_id).prefetch_related(
                    Prefetch(
                        "tweet",
                        queryset=Tweet.objects.select_related("user").filter(
                            user=account
                        ),
                        to_attr="tweet_account",
                    )
                )
            )[0]
            .tweet.all()
            .order_by("-created_at")
        )
        follow_flg = FollowConnection.objects.filter(
            follower=request.user, following=account
        ).exists()
        return render(
            request,
            "account/account_detail.html",
            {
                "account": account,
                "profile": user_profile,
                "tweet_list": tweet_list,
                "follow_flg": follow_flg,
            },
        )


@login_required
@require_http_methods(["GET"])
def follow_account_view(request, account_id):
    """
    アカウントをフォローするページ
    """

    follower = get_object_or_404(Account, pk=request.user.id)
    following = get_object_or_404(Account, pk=account_id)

    if follower == following:
        return HttpResponseForbidden()

    _, is_create = FollowConnection.objects.get_or_create(
        follower=follower, following=following
    )
    if not is_create:
        return HttpResponseForbidden()

    return redirect(f"/accounts/{account_id}")


@login_required
@require_http_methods(["GET"])
def unfollow_account_view(request, account_id):
    """
    アカウントをフォロー解除するページ
    """

    follower = get_object_or_404(Account, pk=request.user.id)
    following = get_object_or_404(Account, pk=account_id)

    if follower == following:
        return HttpResponseForbidden()
    follow = get_object_or_404(FollowConnection, follower=follower, following=following)
    follow.delete()
    return redirect(f"/accounts/{account_id}")

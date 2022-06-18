from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode

from .forms import SignUpForm, LoginForm, ProfileForm
from .models import Profile

def start_view(request):
    """
    最初にアクセスした際に見れるページ
    """

    return render(request, 'account/start.html')


def register_view(request):
    """
    ユーザ登録をする際にアクセスするページ
    """
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('account:complete'))

    return render(request, 'account/register.html', {'form': form})


def complete_view(request):
    """
    ユーザ登録が完了した際に見れるページ
    """

    return render(request, 'account/complete.html')


def login_view(request):
    """
    ログインをする際に見れるページ
    """
    
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    redirect_url = reverse('account:home')
                    parameters = urlencode({'user': user})
                    url = f'{redirect_url}?{parameters}'
                    return redirect(url)
        return render(request, 'account/login.html', {'form': form})
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def home_view(request):
    """
    ログイン後に遷移するページ（遷移確認のために仮で作成）
    """
    if Profile.objects.filter(user=request.user):
        user_profile = Profile.objects.get(user=request.user)
    else:
        user_profile = ""

    return render(request, 'account/home.html', {'profile': user_profile})


@login_required
def logout_view(request):
    """
    ログアウト後に遷移するページ（ログインページへ戻る）
    """

    logout(request)
    form = LoginForm()
    redirect_url = reverse('account:login')
    parameters = urlencode({'form': form})
    url = f'{redirect_url}?{parameters}'

    return redirect(url)


@login_required
def edit_profile_view(request):
    """
    プロフィールを編集するページ
    """

    if request.method == 'GET':
        form = ProfileForm()
        if Profile.objects.filter(user=request.user):
            user_profile = Profile.objects.get(user=request.user)
        else:
            user_profile = ""
        return render(request, 'account/edit_profile.html', {'form': form, 'profile': user_profile})
    elif request.method == 'POST':
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            profile = form.save(request.user)  # form.save(commit=False)
            if hasattr(request.user, 'profile'):
                request.user.profile.profile = profile.profile
                profile = request.user.profile
            else:
                profile.user = request.user
            profile.save()
        if Profile.objects.filter(user=request.user):
            user_profile = Profile.objects.get(user=request.user)
        else:
            user_profile = ""
        return render(request, 'account/edit_profile.html', {'form': form , 'profile': user_profile})
    return HttpResponseNotAllowed(['GET', 'POST'])

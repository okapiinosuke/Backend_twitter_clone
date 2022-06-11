from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SignUpForm, LoginForm, ProfileForm


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
                    return render(request, 'account/home.html', {'user': user})
    else:
        request_method_error = "GETメソッドとPOSTメソッド以外受け付けていません。"
        return render(request, 'account/login.html', {'form': form, 'request_method_error': request_method_error})


@login_required
def home_view(request):
    """
    ログイン後に遷移するページ（遷移確認のために仮で作成）
    """

    return render(request, 'account/home.html')


@login_required
def logout_view(request):
    """
    ログアウト後に遷移するページ（ログインページへ戻る）
    """

    logout(request)
    form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


@login_required
def profile_view(request):
    """
    プロフィールを編集するページ
    """

    login_user = request.user
    if request.method == 'GET':
        form = ProfileForm()
        return render(request, 'account/profile.html', {'form': form})
    elif request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=login_user)
        if form.is_valid():
            form.save()
        return render(request, 'account/profile.html', {'form': form})
    else:
        request_method_error = "GETメソッドとPOSTメソッド以外受け付けていません。"
        return render(request, 'account/profile.html', {'form': form, 'request_method_error': request_method_error})

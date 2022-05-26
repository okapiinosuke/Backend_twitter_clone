from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SignUpForm, LoginForm


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
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get['username']
            password = form.cleaned_data.get['password']
            user = authenticate(username=username, password=password)
            if user:
                print('ok')
                if user.is_active:
                    login(request, user)
                    return render(request, 'account/home.html', {'user': user})
    #form.add_error(None, 'LOGIN_ID、またはPASSWORDが違います。')

    return render(request, 'account/login.html', {'form': form})


@login_required
def home_view(request):
    """
    ログイン後に遷移するページ（遷移確認のために仮で作成）
    """

    return render(request, 'account/home.html')


@login_required
def logout_view(request):
    logout(request)
    form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

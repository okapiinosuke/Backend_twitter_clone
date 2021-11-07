from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from .forms import SignUpForm


def start(request):
    """
    最初にアクセスした際に見れるページ
    """

    return render(request, 'account/start.html')


def register(request):
    """
    ユーザ登録をする際にアクセスするページ
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/register/complete')
    else:
        form = SignUpForm()

    return render(request, 'account/register.html', {'form': form})


def complete(request):
    """
    ユーザ登録が完了した際に見れるページ
    """

    return render(request, 'account/complete.html')


def login(request):
    """
    ログインをする際に見れるページ（遷移確認のために仮で作成）
    """

    return render(request, 'account/login.html')

from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SignUpForm


def start_view(request):
    """
    最初にアクセスした際に見れるページ
    """

    return render(request, 'account/start.html')


def register_view(request):
    """
    ユーザ登録をする際にアクセスするページ
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            state = "complete"
            return redirect(reverse('account:complete'))
    else:
        form = SignUpForm()

    return render(request, 'account/register.html', {'form': form})


def complete_view(request):
    """
    ユーザ登録が完了した際に見れるページ
    """

    return render(request, 'account/complete.html')


def login_view(request):
    """
    ログインをする際に見れるページ（遷移確認のために仮で作成）
    """

    return render(request, 'account/login.html')

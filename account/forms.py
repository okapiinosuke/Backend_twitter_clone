from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import (EmailValidator, MaxLengthValidator,
                                    MinLengthValidator)

from .models import Account


class SignUpForm(UserCreationForm):
    """
    ユーザ作成用フォーム
    """

    email = forms.CharField(
        required=True,
        label='メールアドレス',
        error_messages={'required': 'Please enter your email'},
        validators=[EmailValidator()])
    username = forms.CharField(
        required=True,
        label='ユーザ名',
        help_text='文字数は，1文字以上30文字以下です．',
        error_messages={'required': 'Please enter your username'},
        validators=[MinLengthValidator(1),
        MaxLengthValidator(30)])
    password1 = forms.CharField(
        required=True,
        label='パスワード',
        help_text='文字数は，8文字以上20文字以下です．',
        error_messages={'required': 'Please enter your password1'},
        validators=[MinLengthValidator(8),
        MaxLengthValidator(20)],
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        required=True,
        label='パスワードの再入力',
        help_text='もう一度同じパスワードを入力してください．',
        error_messages={'required': 'Please enter your password2'},
        validators=[MinLengthValidator(8),
        MaxLengthValidator(20)],
        widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        """
        パスワード2がパスワード1と一致するかどうか確認する
        """

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

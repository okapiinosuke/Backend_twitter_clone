from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import (EmailValidator, MaxLengthValidator,
                                    MinLengthValidator)
from django.utils.translation import gettext_lazy as _

from .models import Account


class SignUpForm(UserCreationForm):
    """
    ユーザ作成用フォーム
    """

    email = forms.CharField(
            required=True,
            label=_('Email'),
            error_messages={'required': 'メールアドレスを入れて下さい．'},
            validators=[EmailValidator(), MaxLengthValidator(200)])
    username = forms.CharField(
        required=True,
        label=_('username'),
        help_text='文字数は，1文字以上30文字以下です．',
        error_messages={'required': 'ユーザー名を入れて下さい．'},
        validators=[MinLengthValidator(1),
            MaxLengthValidator(30)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].required = True
        self.fields['password2'].required = True

        self.fields['password1'].help_text = '文字数は，8文字以上20文字以下です．'
        self.fields['password2'].help_text = 'もう一度同じパスワードを入力してください．'

        self.fields['password1'].error_messages = {'required': 'パスワードを入れて下さい．'}
        self.fields['password2'].error_messages = {'required': 'もう一度同じパスワードを入力してください．'}

        self.fields['password1'].validators = [MinLengthValidator(8), MaxLengthValidator(20)]
        self.fields['password2'].validators = [MinLengthValidator(8), MaxLengthValidator(20)]

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    ログインフォーム
    """
    username = forms.CharField(
        required=True,
        label=_('username'),
        error_messages={'required': 'ユーザー名を入れて下さい．'},
        validators=[MinLengthValidator(1),
            MaxLengthValidator(30)])
    password = forms.CharField(
        required=True,
        label=_("password"),
        error_messages={'required': 'パスワードを入れて下さい．'},
        widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProfileForm(forms.ModelForm):
    """
    プロフィールフォーム
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Account
        fields = {'profile'}
        widgets = {
            'profile': forms.Textarea
        }
        labels = {
            'profile': 'プロフィール'
        }

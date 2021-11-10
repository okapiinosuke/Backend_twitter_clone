import re

from django.test import Client, TestCase
from django.urls import reverse

from .models import Account
from .forms import SignUpForm


class RegistrationTest(TestCase):
    """
    登録機能に対するテスト
    """

    def setUp(self):
        self.path = reverse('account:register')

    def test_correct_form(self):
        """
        正しいフォームの場合
        """

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(
            path=self.path,
            data={
                'email': 'sample@example.com',
                'username': 'sample',
                'password1': 'instance1',
                'password2': 'instance1',
            }
        )

        # form

        saved_accounts = Account.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(saved_accounts.count(), 1)

        filtered_accounts = Account.objects.filter(email="sample@example.com")
        self.assertEqual(filtered_accounts.count(), 1)


    def test_is_lack_of_username(self):
        """
        ユーザ名を入れ忘れた場合
        """
        
        data = {
            'email': 'sample@example.com',
            'username': '',
            'password1': 'instance1',
            'password2': 'instance1',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['username'][0], "ユーザ名を入れて下さい．")
    
    def test_is_too_long_username(self):
        """
        ユーザ名が長すぎる（31文字以上）の場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'samplesamplesamplesamplesamples',
            'password1': 'instance1',
            'password2': 'instance1',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertIn("この値は 30 文字以下でなければなりません", f.errors['username'][0])
    
    def test_is_lack_of_email(self):
        """
        メールアドレスを入れ忘れた場合
        """

        data = {
            'email': '',
            'username': 'sample',
            'password1': 'instance1',
            'password2': 'instance1',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['email'][0], "メールアドレスを入れて下さい．")

    def test_is_invalid_email(self):
        """
        メールアドレスの形式として正しくないものを入れた場合
        """

        data = {
            'email': 'sampleexample.com',
            'username': 'sample',
            'password1': 'instance1',
            'password2': 'instance1',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['email'][0], "有効なメールアドレスを入力してください。")

    def test_is_lack_of_password(self):
        """
        パスワードを入れ忘れた場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': '',
            'password2': '',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['password1'][0], "パスワードを入れて下さい．")
        self.assertEqual(f.errors['password2'][0], "もう一度同じパスワードを入力してください．")

    def test_is_too_short_password(self):
        """
        パスワードが短すぎる（7文字以下）場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': 'instanc',
            'password2': 'instanc',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertIn("この値が少なくとも 8 文字以上であることを確認してください", f.errors['password1'][0])
        self.assertIn("この値が少なくとも 8 文字以上であることを確認してください", f.errors['password2'][0])

    def test_is_too_long_password(self):
        """
        パスワードが長すぎる（21文字以上）場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': 'toolonginstancepasswo',
            'password2': 'toolonginstancepasswo',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertIn("この値は 20 文字以下でなければなりません", f.errors['password1'][0])
        self.assertIn("この値は 20 文字以下でなければなりません", f.errors['password2'][0])

    def test_password2_is_different_from_password1(self):
        """
        パスワード1とパスワード2が異なる場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': 'instance1',
            'password2': 'instance2',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['password2'][0], "確認用パスワードが一致しません。")

    def test_password_is_too_simple(self):
        """
        パスワードが安直な場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': 'aaaa1111',
            'password2': 'aaaa1111',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['password2'][0], "このパスワードは一般的すぎます。")

    def test_password2_is_similar_to_username(self):
        """
        パスワードがユーザ名に似過ぎている場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': 'sample11',
            'password2': 'sample11',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['password2'][0], "このパスワードは ユーザー名 と似すぎています。")

    def test_password_is_only_number(self):
        """
        パスワードが数値だけの場合
        """

        data = {
            'email': 'sample@example.com',
            'username': 'sample',
            'password1': '19981104',
            'password2': '19981104',
        }

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors['password2'][0], "このパスワードは数字しか使われていません。")

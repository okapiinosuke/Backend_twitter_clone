from django.http import HttpResponseNotAllowed
from django.test import TestCase
from django.urls import reverse

from .models import Account, Profile, FollowConnection
from .forms import SignUpForm, LoginForm


class RegistrationTest(TestCase):
    """
    登録機能に対するテスト
    """

    def setUp(self):
        self.path = reverse("account:register")

    def test_correct_form(self):
        """
        正しいフォームの場合
        """

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(
            path=self.path,
            data={
                "email": "sample@example.com",
                "username": "sample",
                "password1": "instance1",
                "password2": "instance1",
            },
        )

        saved_accounts = Account.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(saved_accounts.count(), 1)

        filtered_accounts = Account.objects.filter(email="sample@example.com")
        self.assertEqual(filtered_accounts.count(), 1)

    def test_is_lack_of_username(self):
        """
        ユーザー名を入れ忘れた場合
        """

        data = {
            "email": "sample@example.com",
            "username": "",
            "password1": "instance1",
            "password2": "instance1",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["username"][0], "ユーザー名を入れて下さい．")

    def test_is_too_long_username(self):
        """
        ユーザー名が長すぎる（31文字以上）の場合
        """

        data = {
            "email": "sample@example.com",
            "username": "samplesamplesamplesamplesamples",
            "password1": "instance1",
            "password2": "instance1",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertIn("この値は 30 文字以下でなければなりません", f.errors["username"][0])

    def test_is_lack_of_email(self):
        """
        メールアドレスを入れ忘れた場合
        """

        data = {
            "email": "",
            "username": "sample",
            "password1": "instance1",
            "password2": "instance1",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["email"][0], "メールアドレスを入れて下さい．")

    def test_is_invalid_email(self):
        """
        メールアドレスの形式として正しくないものを入れた場合
        """

        data = {
            "email": "sampleexample.com",
            "username": "sample",
            "password1": "instance1",
            "password2": "instance1",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["email"][0], "有効なメールアドレスを入力してください。")

    def test_is_lack_of_password(self):
        """
        パスワードを入れ忘れた場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "",
            "password2": "",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password1"][0], "パスワードを入れて下さい．")
        self.assertEqual(f.errors["password2"][0], "もう一度同じパスワードを入力してください．")

    def test_is_too_short_password(self):
        """
        パスワードが短すぎる（7文字以下）場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "instanc",
            "password2": "instanc",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertIn("この値が少なくとも 8 文字以上であることを確認してください", f.errors["password1"][0])
        self.assertIn("この値が少なくとも 8 文字以上であることを確認してください", f.errors["password2"][0])

    def test_is_too_long_password(self):
        """
        パスワードが長すぎる（21文字以上）場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "toolonginstancepasswo",
            "password2": "toolonginstancepasswo",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertIn("この値は 20 文字以下でなければなりません", f.errors["password1"][0])
        self.assertIn("この値は 20 文字以下でなければなりません", f.errors["password2"][0])

    def test_password2_is_different_from_password1(self):
        """
        パスワード1とパスワード2が異なる場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "instance1",
            "password2": "instance2",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "確認用パスワードが一致しません。")

    def test_password_is_too_simple(self):
        """
        パスワードが安直な場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "aaaa1111",
            "password2": "aaaa1111",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "このパスワードは一般的すぎます。")

    def test_password2_is_similar_to_username(self):
        """
        パスワードがユーザー名に似過ぎている場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "sample11",
            "password2": "sample11",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "このパスワードは ユーザー名 と似すぎています。")

    def test_password_is_only_number(self):
        """
        パスワードが数値だけの場合
        """

        data = {
            "email": "sample@example.com",
            "username": "sample",
            "password1": "19981104",
            "password2": "19981104",
        }

        saved_accounts = Account.objects.all()
        self.assertEqual(saved_accounts.count(), 0)

        response = self.client.post(path=self.path, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saved_accounts.count(), 0)

        f = SignUpForm(data)

        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "このパスワードは数字しか使われていません。")


class LoginTest(TestCase):
    """
    ログイン機能に対するテスト
    """

    def setUp(self):
        Account.objects.create_user(
            email="sample@example.com", username="sample", password="instance1"
        )
        self.path = reverse("account:login")

    def test_correct_login(self):
        """
        正しくログインした場合
        """

        self.assertEqual(Account.objects.all().count(), 1)

        login = self.client.login(username="sample", password="instance1")

        self.assertTrue(login)

        response = self.client.post(
            path=self.path, data={"username": "sample", "password": "instance1"}
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue("/home/", response["location"][0])

    def test_incorrect_password(self):
        """
        間違ったパスワードを入力した場合
        """

        self.assertEqual(Account.objects.all().count(), 1)

        login = self.client.login(username="sample", password="instance2")
        self.assertFalse(login)

        response = self.client.post(
            path=self.path, data={"username": "sample", "password": "instance2"}
        )
        self.assertEqual(response.status_code, 200)

        form = LoginForm(data={"username": "sample", "password": "instance2"})
        self.assertEqual(
            form.errors["__all__"][0],
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )

    def test_not_registered_account(self):
        """
        登録していないアカウントの情報を入力した場合
        """

        self.assertEqual(Account.objects.all().count(), 1)

        login = self.client.login(username="example", password="instance10")
        self.assertFalse(login)

        response = self.client.post(
            path=self.path, data={"username": "example", "password": "instance10"}
        )
        self.assertEqual(response.status_code, 200)

        form = LoginForm(data={"username": "example", "password": "instance10"})
        self.assertEqual(
            form.errors["__all__"][0],
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )

    def test_other_requests(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class LogoutTest(TestCase):
    """
    ログアウト機能に対するテスト
    """

    def setUp(self):
        Account.objects.create_user(
            email="sample@example.com", username="sample", password="instance1"
        )
        self.client.login(username="sample", password="instance1")

    def test_normal_logout(self):
        """
        ログインしているアカウントから正しくログアウトした場合
        """
        response = self.client.get(path=reverse("account:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse("username" in response.context)


class EditProfileTest(TestCase):
    """
    プロフィール編集機能に対するテスト
    """

    def setUp(self):
        Account.objects.create_user(
            email="sample1@example.com", username="sample1", password="instance1"
        )
        Profile.objects.create(user=Account.objects.get(username="sample1"))
        self.client.login(username="sample1", password="instance1")
        self.path = reverse("account:edit_profile")

    def test_correct_editing_profile(self):
        """
        正しくプロフィールを編集した場合
        """

        self.assertEqual(Profile.objects.all().count(), 1)
        response = self.client.post(path=self.path, data={"profile": "sample1です。"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["user"], Profile.objects.get(profile="sample1です。").user
        )

    def test_other_requests(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class FollowTest(TestCase):
    """
    フォロー機能に対するテスト
    """

    def setUp(self):
        Account.objects.create_user(
            email="sample1@example.com", username="sample1", password="instance1"
        )
        Profile.objects.create(user=Account.objects.get(username="sample1"))
        Account.objects.create_user(
            email="sample2@example.com", username="sample2", password="instance2"
        )
        Profile.objects.create(user=Account.objects.get(username="sample2"))
        self.follower_user = Account.objects.get(username="sample1")
        self.followee_user = Account.objects.get(username="sample2")
        self.client.login(username="sample1", password="instance1")
        self.path = reverse("account:follow", args=[self.followee_user.id])

    def test_follow_account(self):
        """
        正しくフォローした場合
        """

        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 0)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        self.assertEqual(
            FollowConnection.objects.filter(
                follower=self.follower_user, followee=self.followee_user
            ).count(),
            1,
        )
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 1)

    def test_follow_myself(self):
        """
        自身をフォローした場合
        """

        self.client.login(username="sample2", password="instance2")
        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        self.assertEqual(response.context["followee_num"], 0)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        self.assertEqual(response.context["followee_num"], 0)

    def test_duplicated_follow(self):
        """
        二重でフォローした場合
        """
        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        self.assertEqual(
            FollowConnection.objects.filter(
                follower=self.follower_user, followee=self.followee_user
            ).count(),
            1,
        )
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 1)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 1)

    def test_other_requests(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class UnFollowTest(TestCase):
    """
    フォロー解除機能に対するテスト
    """

    def setUp(self):
        Account.objects.create_user(
            email="sample1@example.com", username="sample1", password="instance1"
        )
        Profile.objects.create(user=Account.objects.get(username="sample1"))
        Account.objects.create_user(
            email="sample2@example.com", username="sample2", password="instance2"
        )
        Profile.objects.create(user=Account.objects.get(username="sample2"))
        self.follower_user = Account.objects.get(username="sample1")
        self.followee_user = Account.objects.get(username="sample2")
        FollowConnection.objects.create(
            follower=self.follower_user, followee=self.followee_user
        )
        self.client.login(username="sample1", password="instance1")
        self.path = reverse("account:unfollow", args=[self.followee_user.id])

    def test_unfollow_account(self):
        """
        正しくフォロー解除した場合
        """

        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 1)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 0)

    def test_unfollow_myself(self):
        """
        自身をフォロー解除した場合
        """

        self.client.login(username="sample2", password="instance2")
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 1)
        self.assertEqual(response.context["followee_num"], 0)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 1)
        self.assertEqual(response.context["followee_num"], 0)

    def test_duplicated_unfollow(self):
        """
        二重でフォロー解除した場合
        """

        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FollowConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["followee_num"], 0)

    def test_unfollow_not_follow_account(self):
        """
        フォローしていない人を解除した場合
        """

        self.client.login(username="sample2", password="instance2")
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["followee_num"], 0)
        response = self.client.post(
            path=reverse("account:unfollow", args=[self.follower_user.id])
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FollowConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.follower_user.id])
        )
        self.assertEqual(response.context["follower_num"], 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.followee_user.id])
        )
        self.assertEqual(response.context["followee_num"], 0)

    def test_other_requests(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

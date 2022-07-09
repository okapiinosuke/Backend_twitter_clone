from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse

from .models import Tweet
from .forms import TweetForm
from account.models import Account, Profile


class TweetTest(TestCase):
    """
    ツイート機能に対するテスト
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
        self.client.login(username="sample1", password="instance1")
        self.path = reverse("account:home")

    def test_correct_tweet(self):
        """
        正しくツイートした場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)

        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.all().count(), 1)

    def test_too_short_tweet(self):
        """
        0文字でツイートした場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": ""})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.all().count(), 0)

        f = TweetForm(data={"content": ""})
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["content"][0], "入力が必須です．")

    def test_too_long_tweet(self):
        """
        255文字より多い文字数でツイートした場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "a" * 256})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.all().count(), 0)

        f = TweetForm(data={"content": "a" * 256})
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["content"][0], "文字数は，255文字以下です．")

    def test_confirm_tweet(self):
        """
        存在するツイートの詳細を確認した場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.all().count(), 1)

        tweet = Tweet.objects.filter(content="Hello, world.")[0]
        response = self.client.get(path=reverse("tweet:tweet_detail", args=[tweet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tweet"], tweet)

    def test_confirm_ghost_tweet(self):
        """
        存在しないツイートの詳細を確認した場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.get(path=redirect("/tweet_1"))
        self.assertEqual(response.status_code, 404)

    def test_delete_tweet(self):
        """
        正しくツイート削除した場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(Tweet.objects.all().count(), 1)
        tweet = Tweet.objects.filter(content="Hello, world.")[0]
        response = self.client.get(path=reverse("tweet:delete_tweet", args=[tweet.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.all().count(), 0)

    def test_delete_tweet_from_others(self):
        """
        作成者以外がツイートの削除をしようとした場合
        """

        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(Tweet.objects.all().count(), 1)
        self.client.login(username="sample2", password="instance2")
        tweet = Tweet.objects.filter(content="Hello, world.")[0]
        response = self.client.get(path=reverse("tweet:delete_tweet", args=[tweet.id]))
        self.assertEqual(response.status_code, 403)

    def test_other_request(self):
        """
        GET及びPOSTメソッド（tweet_detailとdelete_tweetはGETのみ）以外のリクエストを送信した場合
        """
        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(Tweet.objects.all().count(), 1)

        tweet = Tweet.objects.filter(content="Hello, world.")[0]
        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

        response = self.client.post(path=reverse("tweet:tweet_detail", args=[tweet.id]))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

        response = self.client.post(path=reverse("tweet:delete_tweet", args=[tweet.id]))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

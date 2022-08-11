from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse

from .models import Tweet, FavoriteConnection
from .forms import TweetForm
from account.models import Account, Profile


class TweetCreateTest(TestCase):
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

    def test_other_request(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """
        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(Tweet.objects.all().count(), 1)

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class TweetDetailTest(TestCase):
    """
    ツイートの詳細確認機能に対するテスト
    """

    def setUp(self):
        Account.objects.create_user(
            email="sample1@example.com", username="sample1", password="instance1"
        )
        Profile.objects.create(user=Account.objects.get(username="sample1"))
        self.client.login(username="sample1", password="instance1")
        self.path = reverse("account:home")

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
        response = self.client.get(path=redirect("/tweets/1"))
        self.assertEqual(response.status_code, 404)

    def test_other_request(self):
        """
        GETメソッド以外のリクエストを送信した場合
        """
        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(Tweet.objects.all().count(), 1)

        tweet = Tweet.objects.filter(content="Hello, world.")[0]
        response = self.client.put(path=reverse("tweet:tweet_detail", args=[tweet.id]))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class TweetDeleteTest(TestCase):
    """
    ツイート削除機能に対するテスト
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
        GETメソッド以外のリクエストを送信した場合
        """
        self.assertEqual(Tweet.objects.all().count(), 0)
        response = self.client.post(path=self.path, data={"content": "Hello, world."})
        self.assertEqual(Tweet.objects.all().count(), 1)

        tweet = Tweet.objects.filter(content="Hello, world.")[0]
        response = self.client.post(path=reverse("tweet:delete_tweet", args=[tweet.id]))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class FavoriteTest(TestCase):
    """
    いいね機能に対するテスト
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

        self.user1 = Account.objects.get(username="sample1")
        self.user2 = Account.objects.get(username="sample2")

        self.favorited_tweet1 = Tweet.objects.create(user=self.user2, content="aaa")
        self.favorited_tweet2 = Tweet.objects.create(user=self.user1, content="bbb")

        self.client.login(username="sample1", password="instance1")
        self.path = reverse("tweet:favorite_tweet", args=[self.favorited_tweet1.id])

    def test_favorite_tweet(self):
        """
        正しくいいねした場合
        """

        self.assertEqual(FavoriteConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 0)

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteConnection.objects.all().count(), 1)
        self.assertEqual(
            FavoriteConnection.objects.filter(
                favorite=self.user1, favorited=self.favorited_tweet1
            ).count(),
            1,
        )
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 1)
        self.assertIsNotNone(
            FavoriteConnection.objects.filter(
                favorite=self.user1, favorited=self.favorited_tweet1
            )
        )

        response = self.client.post(
            path=reverse("tweet:favorite_tweet", args=[self.favorited_tweet2.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteConnection.objects.all().count(), 2)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 2)

    def test_duplicated_favorite(self):
        """
        二重でいいねした場合
        """
        self.assertEqual(FavoriteConnection.objects.all().count(), 0)
        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteConnection.objects.all().count(), 1)
        self.assertEqual(
            FavoriteConnection.objects.filter(
                favorite=self.user1, favorited=self.favorited_tweet1
            ).count(),
            1,
        )
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 1)

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(FavoriteConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 1)

    def test_other_requests(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)


class UnFavoriteTest(TestCase):
    """
    いいね解除機能に対するテスト
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

        self.user1 = Account.objects.get(username="sample1")
        self.user2 = Account.objects.get(username="sample2")

        self.favorited_tweet1 = Tweet.objects.create(user=self.user2, content="aaa")
        self.favorited_tweet2 = Tweet.objects.create(user=self.user1, content="bbb")

        FavoriteConnection.objects.create(
            favorite=self.user1, favorited=self.favorited_tweet1
        )
        FavoriteConnection.objects.create(
            favorite=self.user1, favorited=self.favorited_tweet2
        )

        self.client.login(username="sample1", password="instance1")
        self.path = reverse("tweet:unfavorite_tweet", args=[self.favorited_tweet1.id])

    def test_unfavorite_tweet(self):
        """
        正しくいいね解除した場合
        """

        self.assertEqual(FavoriteConnection.objects.all().count(), 2)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 2)

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteConnection.objects.all().count(), 1)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 1)

        response = self.client.post(
            path=reverse("tweet:unfavorite_tweet", args=[self.favorited_tweet2.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteConnection.objects.all().count(), 0)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 0)

    def test_duplicated_unfavorite(self):
        """
        二重でいいね解除した場合
        """

        self.assertEqual(FavoriteConnection.objects.all().count(), 2)

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(FavoriteConnection.objects.all().count(), 1)

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FavoriteConnection.objects.all().count(), 1)

        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user1.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 1)

    def test_unfavorite_not_favorite_tweet(self):
        """
        いいねしていないツイートを解除した場合
        """

        self.client.login(username="sample2", password="instance2")
        self.assertEqual(FavoriteConnection.objects.all().count(), 2)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user2.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 0)

        response = self.client.post(
            path=reverse("tweet:unfavorite_tweet", args=[self.favorited_tweet1.id])
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(FavoriteConnection.objects.all().count(), 2)
        response = self.client.get(
            path=reverse("account:account_detail", args=[self.user2.id])
        )
        self.assertEqual(response.context["favorite_connection_list"].count(), 0)

    def test_other_requests(self):
        """
        GET及びPOSTメソッド以外のリクエストを送信した場合
        """

        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

from django.urls import path

from . import views

app_name = "account"


urlpatterns = [
    path("", views.start_view, name="start"),
    path("register/", views.register_view, name="register"),
    path("register/complete/", views.complete_view, name="complete"),
    path("login/", views.login_view, name="login"),
    path("home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),
    path(
        "accounts/<int:account_id>/", views.account_detail_view, name="account_detail"
    ),
    path(
        "accounts/<int:account_id>/follow/",
        views.follow_account_view,
        name="follow",
    ),
    path(
        "accounts/<int:account_id>/unfollow/",
        views.unfollow_account_view,
        name="unfollow",
    ),
    path(
        "accounts/<int:account_id>/followings/",
        views.account_followings_view,
        name="followings",
    ),
    path(
        "accounts/<int:account_id>/followers/",
        views.account_followers_view,
        name="followers",
    ),
]

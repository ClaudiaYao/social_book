from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("settings/", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),
    path("like_post/<str:post_id>", views.like_post, name="like_post"),
    path("profile/<str:profile_id>", views.profile, name="profile"),
    path("follow/<str:followed_profile_id>", views.follow, name="follow"),
    path("search/", views.search, name="search"),
    # path("edit_profile/<str:post_id>", views.edit_post, name="edit_post"),

]

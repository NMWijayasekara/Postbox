from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("create_post", views.create_post, name="create_post"),
    path("edit_post/<str:post_id>", views.edit_post, name="edit_post"),
    path("comment_post/<str:post_id>", views.comment_post, name="comment_post"),
    path("user/<str:username>", views.user_profile, name="user_profile"),
    path("like", views.like, name="like"),
    path("unlike", views.unlike, name="unlike"),
    path("myprofile", views.myprofile, name="my_profile"),
    path("follow",views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

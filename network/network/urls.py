
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('posts/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.follow_toggle, name="follow_toggle"),

]


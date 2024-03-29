from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (  # CreatePostAPIView,
    ChangePasswordView,
    CommentViewSet,
    FollowAPIView,
    LikeAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    TimeLineAPIView,
    TweetViewSet,
    UserViewSet,
)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("posts", TweetViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    # path('create_tweet/', CreatePostAPIView.as_view(), name='createtweet'),
    path("follow/", FollowAPIView.as_view(), name="follow"),
    path("home/", TimeLineAPIView.as_view(), name="home"),
    path("like/", LikeAPIView.as_view(), name="likes"),
    path("password_change/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "password_reset/",
        PasswordResetAPIView.as_view(),
        name="password_reset_email_send",
    ),
    path(
        "password_reset_confirm/<uuid:code>/",
        PasswordResetConfirmAPIView.as_view(),
        name="password_reset_confirm",
    ),
    path("", include(router.urls)),
]

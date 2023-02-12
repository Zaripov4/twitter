from django.urls import path, include
from .views import (
    UserViewSet,
    TweetListViewSet,
    CreatePostAPIView,
    LikeAPIView,
    FollowAPIView,
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('list', TweetListViewSet)

urlpatterns = [
    path('create_tweet/', CreatePostAPIView.as_view(), name='createtweet'),
    path('like/', LikeAPIView.as_view(), name='like_tweet'),
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('', include(router.urls)),
]

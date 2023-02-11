from django.urls import path, include
from .views import (
    UserViewSet,
    TweetListViewSet,
    create_post,
    LikeAPIView,
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', UserViewSet)
router.register('list/', TweetListViewSet)

urlpatterns = [
    path('create_tweet/', create_post, name='createtweet'),
    path('like/<int:pk>', LikeAPIView.as_view(), name='like_tweet'),
    path('', include(router.urls)),
]

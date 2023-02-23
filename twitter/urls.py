from django.urls import path, include
from .views import (
    UserViewSet,
    TweetListViewSet,
    # CreatePostAPIView,
    LikeAPIView,
    FollowAPIView,
    TimeLineAPIView,
    CommentViewSet,
    CreatePostViewSet,
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('list', TweetListViewSet)
router.register('comment', CommentViewSet)
router.register('create', CreatePostViewSet)

urlpatterns = [
    # path('create_tweet/', CreatePostAPIView.as_view(), name='createtweet'),
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('home/', TimeLineAPIView.as_view(), name='home'),
    path('like/', LikeAPIView.as_view(), name='likes'),
    path('', include(router.urls)),
]

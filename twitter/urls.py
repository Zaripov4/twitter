from django.urls import path, include
from .views import (
    UserViewSet,
    TweetListView,
    create_post,
    LikeView,
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('home/', TweetListView.as_view(), name='home'),
    path('create_tweet/', create_post, name='createtweet'),
    path('like/<int:pk>', LikeView, name='like_tweet'),
]
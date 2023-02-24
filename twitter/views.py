from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .serializers import (
    UserSerializer, 
    UserListSerializer, 
    UserCreateSerializer, 
    PostListSerializer,
    FileListSerializer,
    CommentSerializer,
    PostCreateSerializer,
)
from .models import (
    User, 
    Post, 
    File, 
    Follow, 
    Like,
    Comment,
)
from django.views import generic
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]    
        return super(UserViewSet,self).get_permissions()

    def get_serializer_class(self):
        serializer_map = {
            'create': UserCreateSerializer,
            'list': UserListSerializer,
        }
        return serializer_map.get(self.action, UserSerializer)

    def get_queryset(self):
        return super().get_queryset()

class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    ordering = ['-id']

    def get_queryset(self):
        return super().get_queryset()
    

class LikeAPIView(APIView): 
    def post(self, request, *args, **kwargs):    
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        if request.user != post.author:
            post.liked_by_author = request.user == post.author
            post.save()
            return Response(status=status.HTTP_200_OK)
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.save()
        else:
            post.likes.add(request.user)
            post.save()

    # def like_tweet(request, post_id):
    #     tweet = get_object_or_404(Post, pk=post_id)
    #     if request.user != tweet.user:
    #         tweet.liked_by_author = request.user == tweet.user
    #         tweet.save()
    #     return Response(status=status.HTTP_200_OK)
    
    # def unlike_tweet(request, post_id):
    #     tweet = get_object_or_404(Post, pk=post_id)
    #     tweet.liked_by_users.remove(request.user)
    #     tweet.liked_by_author = request.user == tweet.user
    #     tweet.save()
    #     return Response(status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        following_user = User.objects.get(id=user_id)
        follow, created = Follow.objects.get_or_create(
            user1=following_user,
            user2=request.user
        )
        if not created:
            follow.delete()
        return Response(status=status.HTTP_200_OK)

class TimeLineAPIView(APIView):
    def get(self, request):
        user_follows = Follow.objects.filter(user2__id=request.user.id).values_list('user1', flat=True)
        tweets = Post.objects.filter(author__in=user_follows).order_by('-create_date')
        serializer = PostListSerializer(tweets, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

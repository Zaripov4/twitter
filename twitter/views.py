from django.shortcuts import render, get_object_or_404, redirect
from .serializers import (
    UserSerializer, 
    UserListSerializer, 
    UserCreateSerializer, 
    PostListSerializer,
    FileListSerializer
)
from .models import User, Post, File, Follow
from django.views import generic
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

class UserViewSet(viewsets.ModelViewSet):
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

class TweetListViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    ordering = ['-create_date']

    def get_queryset(self):
        return super().get_queryset()


class LikeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.save()
        else:
            post.likes.add(request.user)
            post.save()
        return Response(status=status.HTTP_200_OK)

class CreatePostAPIView(APIView):
    def post(request):
        if request.method == 'POST':
            author = request.user
            post_form = PostListSerializer()
            file_form = FileListSerializer()
            files = request.FILES.getlist('file')
            if post_form.is_valid() and file_form.is_valid():
                post_instance = post_form.save(commit=True)
                post_instance.author = author
                post_instance.save()
                
                file_instamce = file_form.save(commit=True)
                for f in files:
                    file_instamce.post = File(file=f, post=post_instance).save()
                return PostListSerializer(data=post_instance)
            return ValidationError(
                detail='Error'
            )

class FollowAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        following_user = User.objects.get(id=user_id)
        follow, created = Follow.objects.get_or_create(
            following=following_user,
            follower=request.user
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

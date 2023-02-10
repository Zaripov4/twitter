from django.shortcuts import render, get_object_or_404, redirect
from .serializers import (
    UserSerializer, 
    UserListSerializer, 
    UserCreateSerializer, 
    PostListSerializer,
    FileListSerializer
)
from .models import User, Post, File
from django.views import generic
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

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

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    linked = False
    if post.likes.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True

class TweetListView(generic.ListView):
    model = Post
    ordering = ['-created_date']

def create_post(request):
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
        return PostListSerializer
    else:
        post_form = PostListSerializer()
        file_form = FileListSerializer()
        return create_post()

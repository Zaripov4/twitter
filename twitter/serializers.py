from rest_framework import serializers
from . models import User, Post, File, Like
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'followers',
            'follows',
        )

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class PostListSerializer(serializers.ModelSerializer):
    liked_by_users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = [
            'author',
            'body',
            'create_date',
            'parent',
            'like_count',
            'liked_by_users',
            'likes',
        ]

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

from rest_framework import serializers
from . models import User, Post, File
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
    class Meta:
        model = Post
        fields = '__all__'

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

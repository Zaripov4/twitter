from rest_framework import serializers
from . models import User, Post, File, Like, Comment, ResetCode
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError

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
        fields = [
            'id',
            'author',
            'body',
            'create_date',
            'parent',
            'like_count',
            'liked_by_author',
            'comments',
            'comments_count'
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'body',
            'parent',
            'files',
        ]

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=255)

    extra_kwargs = {
        'password': {'write_only': True, 'min_length': 8,
                     'style': {'input_type': password}}
    }

    def validate(self, attrs):
        password = attrs['password']
        if password:
            try:
                password_validation.validate_password(password, password)
            except:
                raise ValidationError('error')

        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password',
        ]

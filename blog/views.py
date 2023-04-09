import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from service import settings

from .models import Comment, File, Follow, Post, ResetCode, User
from .serializers import (
    ChangePasswordSerializer,
    CommentSerializer,
    FileListSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    PostCreateSerializer,
    PostListSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserSerializer,
)

home_url = "adminsite249@gmail.com"
password_reset_url = home_url + "password_reset_confirm/"
password_reset_msg = "Password reset link {}{}"
password_reset_theme = "Password reset"


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super(UserViewSet, self).get_permissions()

    def get_serializer_class(self):
        serializer_map = {
            "create": UserCreateSerializer,
            "list": UserListSerializer,
        }
        return serializer_map.get(self.action, UserSerializer)

    def get_queryset(self):
        return super().get_queryset()

    @action(methods=["get"], detail=False, url_path="@me")
    def me(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_password_reset(email):
    user = User.objects.filter(email=email).all()
    if not user.exists():
        return

    user = user.first()
    code = uuid.uuid4()
    ResetCode.objects.create(user=user, code=code)
    message = password_reset_msg.format(password_reset_url, code)
    send_mail(
        password_reset_theme,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silenty=False,
    )


class PasswordResetAPIView(APIView):
    """Password reset api to send a reset link to email"""

    permission_classes = [
        AllowAny,
    ]

    @action(detail=False, methods=["post"])
    def password_reset(self, request, *args, **kwargs):
        data = request.data
        serialized = PasswordResetSerializer(data=data)
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serialized.data.get("email")
        send_password_reset(email)
        return Response(
            {"email": email, "message": "Password reset link sent to your email"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    @action(methods=["put"], detail=False)
    def reset_confirm(self, request, *args, **kwargs):
        data = request.data
        serializer = PasswordResetConfirmSerializer(data=data)
        if serializer.is_valid():
            code = kwargs.get("code", None)
            password = serializer.data.get("password")
            obj = get_object_or_404(ResetCode, code=code)
            user = obj.user
            obj.delete()
            user.set_password(password)
            user.save()
            return Response(
                {"msg": "password has been changed succesfully", "email": user.email},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    ordering = ["-id"]

    def get_queryset(self):
        return super().get_queryset()


class LikeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
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


class CreatePostViewSet(ModelViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def post(request):
        if request.method == "POST":
            author = request.user
            post_form = PostListSerializer()
            file_form = FileListSerializer()
            files = request.FILES.getlist("file")
            if post_form.is_valid() and file_form.is_valid():
                post_instance = post_form.save(commit=True)
                post_instance.author = author
                post_instance.save()

                file_instamce = file_form.save(commit=True)
                for f in files:
                    file_instamce.post = File(file=f, post=post_instance).save()
                return PostListSerializer(data=post_instance)
            return ValidationError(detail="Error")


class FollowAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        following_user = User.objects.get(id=user_id)
        follow, created = Follow.objects.get_or_create(
            user1=following_user, user2=request.user
        )
        if not created:
            follow.delete()
        return Response(status=status.HTTP_200_OK)


class TimeLineAPIView(APIView):
    def get(self, request):
        user_follows = Follow.objects.filter(user2__id=request.user.id).values_list(
            "user1", flat=True
        )
        tweets = Post.objects.filter(author__in=user_follows).order_by("-create_date")
        serializer = PostListSerializer(tweets, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

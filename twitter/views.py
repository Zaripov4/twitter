from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer()
    queryset = User.objects.all()

from django.contrib import admin
from .models import User, Post, File

admin.site.register(User)
admin.site.register(Post)
admin.site.register(File)

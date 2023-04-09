from django.contrib import admin

from .models import File, Follow, Post, User

admin.site.register(User)
admin.site.register(Post)
admin.site.register(File)
admin.site.register(Follow)

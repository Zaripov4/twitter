from django.contrib import admin
from .models import User, Post, File, Follow

admin.site.register(User)
admin.site.register(Post)
admin.site.register(File)
admin.site.register(Follow)

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def followers(self):
        return self.follower.all().count()

    @property
    def follows(self):
        return self.following.all().count()
    

    class Meta:
        db_table = 'users'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='author')
    body = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='tweets')

    def __str__(self):
        return str(self.body)
    
    @property
    def like_count(self):
        return self.likes.count()


class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    file = models.FileField(upload_to='static', null=True, blank=True)

    def __str__(self):
        return self.post.body + 'File'

class Follow(models.Model):
    following = models.ForeignKey(User, null=True, related_name='follower', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, null=True, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

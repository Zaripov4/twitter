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
    liked_by_author = models.BooleanField(default=False)

    def __str__(self):
        return self.body[:30]
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def liked_by_users(self):
        return [like.user for like in self.likes.all()]


class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    file = models.FileField(upload_to='static', null=True, blank=True)

    def __str__(self):
        return self.body[:30]

class Follow(models.Model):
    # user2 follows user1
    user1 = models.ForeignKey(
        User, null=True, related_name='user1', on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, null=True, related_name='user2', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user2} follows {self.user1}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} likes {self.tweet}'

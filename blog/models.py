from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def followers(self):
        return self.user1.all().count()

    @property
    def follows(self):
        return self.user2.all().count()
    
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
    def comments_count(self):
        return self.comments.count()
    
    @property
    def comments(self):
        return list(self.comments.order_by('created_on')[:5])

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def liked_by_users(self):
        return [like.user for like in self.likes.all()]
    
    @property
    def files(self):
        return self.file()


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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.content} by {self.user}'

class ResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        ResetCode.objects.filter(user=self.user).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

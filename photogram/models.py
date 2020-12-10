from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="op", null=True)
    caption = models.TextField()
    image = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(default=datetime.now)
    likeCount = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} Profile'


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Following(models.Model):
    follower = models.OneToOneField(User, on_delete=models.CASCADE)
    followingUsers = models.ManyToManyField(User, related_name="followers", blank=True)

    def __str__(self):
        return str(self.follower)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
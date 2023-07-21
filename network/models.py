from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

class User(AbstractUser):
    pass

class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    time = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return f"{self.id}|{self.user} create a post '{self.title}' on {self.time}"

    class Meta:
        ordering = ['-time']
class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    
    def serialize(self):
        return {
            "following": self.following
        }
    class Meta:
        unique_together = ["following", "follower"]

    def __str__(self):
        return f"{self.follower} is following {self.following}"

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="user_comment", on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    time = models.DateTimeField(default=django.utils.timezone.now)
    
    class Meta:
        ordering = ['-time']

class Like(models.Model):
    user = models.ForeignKey(User, related_name="user_like", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_like", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f"{self.user} as liked to {self.post}"

    def serialize(self):
        return {
            "post": self.post
        }
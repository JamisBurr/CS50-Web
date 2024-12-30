from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Allow users to follow other users
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)   

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")  # Add related_name to avoid clash

    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"
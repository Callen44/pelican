from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)
    published_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def str_created_by(self):
        return str(self.created_by)
class Like(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
class Comment(models.Model):
    comment = models.CharField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    published_date = models.DateTimeField('date_published')
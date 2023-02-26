from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
<<<<<<< Updated upstream
    post_title = models.CharField(max_length=200)
    post_body = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.post_title
    def get_id(self):
        return self.id
    def get_body(self):
        return self.post_body
    def get_date(self):
        return self.pub_date
    def get_name(self):
        return self.post_title
    def get_author(self):
        return self.by

=======
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)
    published_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
>>>>>>> Stashed changes
class Like(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
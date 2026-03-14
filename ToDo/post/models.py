from django.db import models

class Post(models.Model):
    title       = models.CharField(max_length=200)
    content     = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE,
                                   related_name='comment_set')
    name       = models.CharField(max_length=100)
    body       = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
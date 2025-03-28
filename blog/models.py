from django.db import models
from accounts.models import User, Profile

# Create your models here.

class BlogTags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    description = models.TextField()
    tags = models.ForeignKey(BlogTags, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='blog_images', default='blog.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    total_views = models.IntegerField(default=0)

    def get_comments(self):
        return self.comments.filter(status=True)
    
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name.user.email
    
    def get_replays(self):
        return self.replays.filter(status=True)
    
class Replay(models.Model):
    comment = models.ForeignKey(Comment, related_name='replays', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name.user.email
    

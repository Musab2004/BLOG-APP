from django.db import models
from accounts.models import User
# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    description=models.CharField(max_length=500,null=True)
    blog_title_image= models.ImageField(upload_to='images/',null=True)
    Category = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    isLiked = models.ManyToManyField(User, related_name='liked_posts')
    class Meta:
        ordering = ['-created_at']



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,null=True)
    text = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_reply = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    isLiked = models.ManyToManyField(User, related_name='liked_comments')
    class Meta:
        ordering = ['-created_at']
class ReportedComments(models.Model):
    user = models.ManyToManyField(User,null=True,related_name="reported_comments")
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=200)
class ReportedBlogPost(models.Model):
    user = models.ManyToManyField(User, null=True,related_name="reported_posts")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,null=True)
    message = models.CharField(max_length=200) 
class Suggestion(models.Model):
    user = models.ManyToManyField(User,null=True,related_name="suggestions")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,null=True)
    text = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_reply = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    isLiked = models.ManyToManyField(User, related_name='liked_suggestions')
    class Meta:
        ordering = ['-created_at']       
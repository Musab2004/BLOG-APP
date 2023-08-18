from django import forms
from blog_home.models import BlogPost
from django.contrib.auth.hashers import make_password
class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['user','title','content','description','blog_title_image','Category']
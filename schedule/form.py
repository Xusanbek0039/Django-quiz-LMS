from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user_have_post', 'post_title', 'post_file', 'post_description', 'company_name']
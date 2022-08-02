from django import forms
from .models import Post


class UserPostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields= ["content"]
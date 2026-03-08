from django import forms
from django.core.exceptions import ValidationError

from .models import Post

MAX_POST_LENGTH = 5000


class UserPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise ValidationError("Post content cannot be empty.")
        if len(content) > MAX_POST_LENGTH:
            raise ValidationError(f"Post content must be {MAX_POST_LENGTH} characters or fewer.")
        return content
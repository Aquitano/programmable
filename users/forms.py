from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile

MAX_PROFILE_IMAGE_SIZE = 2 * 1024 * 1024
ALLOWED_PROFILE_IMAGE_TYPES = {
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
}


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "interest", "age", "programmingLanguage"]
        widgets = {
            "interest": forms.Textarea(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "programmingLanguage": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "programmingLanguage": "Most liked programming language",
        }

    def clean_interest(self):
        return (self.cleaned_data.get("interest") or "").strip()

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is None:
            return age
        if age < 0 or age > 120:
            raise ValidationError("Age must be between 0 and 120.")
        return age

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image

        content_type = getattr(image, "content_type", None)
        if content_type and content_type.lower() not in ALLOWED_PROFILE_IMAGE_TYPES:
            raise ValidationError("Please upload a PNG, JPG, GIF, or WebP image.")

        if image.size > MAX_PROFILE_IMAGE_SIZE:
            raise ValidationError("Profile images must be 2 MB or smaller.")

        return image
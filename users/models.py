from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    interest = models.TextField(default="NO INFO", blank=True)
    age = models.IntegerField(default="0")
    programmingLanguage = models.TextField(
        default="NO INFO",
        blank=True,
        choices=[
            ("Python", "Python"),
            ("Java", "Java"),
            ("Visual Basic", "Visual Basic"),
        ],
    )
    followers = models.ManyToManyField(User, related_name="followers")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.image or not hasattr(self.image, "path"):
            return

        try:
            with Image.open(self.image.path) as img:
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.image.path)
        except OSError:
            return

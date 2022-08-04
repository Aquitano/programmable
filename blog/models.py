from itertools import count
import os
from tkinter import CASCADE

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


# TODO create a model for Posts

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.TextField(default="Err")
    content = models.TextField()
    date_published = models.DateField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="posts")

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)   

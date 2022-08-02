from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post
from .forms import UserPostForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'about.html', {'title': 'About'})

def NewPostView(request):
    form = UserPostForm(request.POST or None)

    if request.method == "POST":
            if form.is_valid():
                    form.instance.user = request.user
                    form.instance.username = request.user.username
                    form.save()
            return HttpResponseRedirect("/")
    
    context = {'form': form,}

    return render(request, 'blog/post_form.html', context)

class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    fields = ["content"]

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])


def PostsListView(request):
    allposts = Post.objects.all()

    context = {'allposts': allposts,}
    
    return render(request, 'Blog/userposts-list-view.html', context)

def UserPostsListView(request):
    allposts = Post.objects.filter(user="3")

    context = {'allposts': allposts,}
    
    return render(request, 'Blog/userposts-list-view.html', context)

def PostsDetailView(request, url=None):
    post = get_object_or_404(Post, url=url)

    context = {'post': post,}
    
    return render(request, 'Blog/userposts-detail-view.html', context)
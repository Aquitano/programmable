from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from users.models import Profile
from .models import Post
from .forms import UserPostForm


def home(request):
    posts = Post.objects.all().order_by('-id')
    liked_posts = []

    for post in range(len(posts)):
        if request.user in posts[post].likes.all():
            liked_posts.append(post + 1)

    context = {
        'posts': posts,
        'liked_posts': liked_posts,
    }
    return render(request, 'blog/home.html', context)


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UserPostForm
    template_name = "blog/post_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])

class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    form_class = UserPostForm

    def form_valid(self, form):
        form.instance.content = form.instance.content.replace("script", "s").replace("style", "s")
        return super().form_valid(form)

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

@login_required
def liked_posts_view(request):
    all_user = Profile.objects.all()
    filter_posts = []

    for user in all_user:
        if request.user in user.followers.all():
            filter_posts.append(user)

    context = {
        'posts': filter_posts,
    }

    return render(request, 'blog/following.html', context)

@login_required
def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog-home'))


@login_required
def unlike_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.likes.remove(request.user)

    return HttpResponseRedirect(reverse('blog-home'))
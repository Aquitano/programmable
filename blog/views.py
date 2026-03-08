from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, UpdateView

from users.models import Profile

from .forms import UserPostForm
from .models import Post


def _get_redirect_target(request, fallback_name, *fallback_args):
    next_url = request.POST.get("next")
    allowed_hosts = {request.get_host()}
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts=allowed_hosts,
        require_https=request.is_secure(),
    ):
        return next_url
    return reverse(fallback_name, args=fallback_args)


def home(request):
    posts = Post.objects.select_related("user", "user__profile").prefetch_related("likes").order_by("-id")
    liked_post_ids = set()

    if request.user.is_authenticated:
        liked_post_ids = set(request.user.posts.values_list("id", flat=True))

    context = {
        "posts": posts,
        "liked_post_ids": liked_post_ids,
    }
    return render(request, "blog/home.html", context)


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
    followed_profiles = Profile.objects.filter(followers=request.user).select_related("user", "user__profile")

    context = {
        "profiles": followed_profiles,
    }

    return render(request, "blog/following.html", context)


@login_required
@require_POST
def like_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.likes.add(request.user)
    return redirect(_get_redirect_target(request, "blog-home"))


@login_required
@require_POST
def unlike_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.likes.remove(request.user)
    return redirect(_get_redirect_target(request, "blog-home"))
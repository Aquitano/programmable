from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView

from blog.models import Post

from .forms import ProfileUpdateForm, UserRegisterForm
from .models import Profile


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


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(
                request,
                "Your account has been created. You can log in now.",
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request, username: str):
    profile = get_object_or_404(Profile.objects.select_related("user"), user__username=username)
    user_posts = Post.objects.filter(user=profile.user).annotate(total_likes=Count("likes")).order_by("-id")
    liked_post_ids = set()

    if request.user.is_authenticated:
        liked_post_ids = set(user_posts.filter(likes=request.user).values_list("id", flat=True))

    is_following = request.user.is_authenticated and profile.followers.filter(pk=request.user.pk).exists()
    is_own_profile = request.user.username == username
    context = {
        "profile": profile,
        "user_posts": user_posts,
        "liked_post_ids": liked_post_ids,
        "is_following": is_following,
        "is_own_profile": is_own_profile,
    }
    return render(request, template_name="users/profile.html", context=context)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = "users/user_update.html"
    fields = ["first_name", "last_name", "email"]

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])


class ProfileUpdateStatus(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = "users/profile_update.html"
    form_class = ProfileUpdateForm

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])


@login_required
@require_POST
def follow_view(request, pk):
    profile = get_object_or_404(Profile.objects.select_related("user"), user_id=pk)

    if profile.user == request.user:
        messages.error(request, "You cannot follow your own profile.")
        return redirect(_get_redirect_target(request, "profile", profile.user.username))

    profile.followers.add(request.user)
    messages.success(request, f"You are now following {profile.user.username}.")
    return redirect(_get_redirect_target(request, "profile", profile.user.username))


@login_required
@require_POST
def unfollow_view(request, pk):
    profile = get_object_or_404(Profile.objects.select_related("user"), user_id=pk)

    if profile.user == request.user:
        messages.error(request, "You cannot unfollow your own profile.")
        return redirect(_get_redirect_target(request, "profile", profile.user.username))

    profile.followers.remove(request.user)
    messages.success(request, f"You unfollowed {profile.user.username}.")
    return redirect(_get_redirect_target(request, "profile", profile.user.username))
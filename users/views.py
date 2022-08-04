from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.db.models import F, Count, Func

from blog.models import Post

from .forms import UserRegisterForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username: str):
    """
    View to show the user’s own profile
    """
    profile = Profile.objects.get(user__username=username)
    user_posts = Post.objects.filter(username=username).annotate(total_likes=Count('likes')).order_by('-id')
    liked_posts = []
    
    for post in range(len(user_posts)):
        if request.user in user_posts[post].likes.all():
            liked_posts.append(post+1)
    
    if request.user in profile.followers.all():
        is_Following = True
    else:
        is_Following = False

    print(is_Following)

    is_own_profile = request.user.username == username
    context = {
        'profile': profile,
        'user_posts': user_posts,
        'liked_posts': liked_posts,
        'is_Following': is_Following,
        'is_own_profile': is_own_profile,
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
    fields = ["interest", "image", "age", "programmingLanguage"]

    def test_func(self):
        return self.request.user == self.get_object().user

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])

@login_required
def FollowView(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get('user-id'))
    profile.followers.add(request.user)

    messages.success(request, f'Followed user {profile.user.username}!')

    return HttpResponseRedirect(reverse("profile", args=[profile.user.username]))

@login_required
def UnfollowView(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get('user-id'))
    profile.followers.remove(request.user)

    messages.success(request, f'Unfollowed user {profile.user.username}!')

    return HttpResponseRedirect(reverse("profile", args=[profile.user.username]))
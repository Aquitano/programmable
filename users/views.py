from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView

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
    is_own_profile = request.user.username == username

    context = {
        'profile': profile,
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

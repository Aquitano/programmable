from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from users.models import Profile

from .models import Post
from .forms import UserPostForm

def home(request):
    posts = Post.objects.all().order_by('-date_published')
    liked_posts = []
    
    for post in range(len(posts)):
        if request.user in posts[post].likes.all():
            liked_posts.append(post+1)

    context = {
        'posts': posts,
        'liked_posts': liked_posts,
    }
    return render(request, 'blog/home.html', context)

@login_required
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


# def PostsListView(request):
#     allposts = Post.objects.all()

#     context = {'allposts': allposts,}
    
#     return render(request, 'Blog/userposts-list-view.html', context)

def UserPostsListView(request):
    allposts = Post.objects.filter()

    context = {'allposts': allposts,}
    
    return render(request, 'Blog/userposts-list-view.html', context)

@login_required
def LikedPostsListView(request):
    alluser = Profile.objects.all()
    current = get_object_or_404(Profile, id=request.user.profile.id)
    filter_posts = []

    for user in alluser:
        if request.user in user.followers.all():
            filter_posts.append(user)

    context = {'posts': filter_posts,}
    
    return render(request, 'blog/following.html', context)

# def PostsDetailView(request, url=None):
#     post = get_object_or_404(Post, url=url)

#     context = {'post': post,}
    
#     return render(request, 'Blog/userposts-detail-view.html', context)

@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog-home'))

@login_required
def UnlikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.likes.remove(request.user)

    return HttpResponseRedirect(reverse('blog-home'))
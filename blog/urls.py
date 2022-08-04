from django.urls import path

from blog import views
import blog.views as blog_view

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('following/', views.LikedPostsListView, name='following'),

    # TODO Add all Urls for posts: Create, Update, Delete
    path('create-post/', views.NewPostView, name='new-post'),
    path('edit-post/<int:pk>/', blog_view.EditPostView.as_view(), name='edit-post'),
    path('delete-post/<int:pk>/', blog_view.DeletePostView.as_view(), name='delete-post'),
    path('like/<int:pk>/', blog_view.LikeView, name='like-post'),
    path('unlike/<int:pk>/', blog_view.UnlikeView, name='unlike-post'),
]

from django.contrib.auth import views as auth_views
from django.urls import path
import users.views as user_views

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
    path('register/', user_views.register, name='register'),
    path('profile/<str:username>/', user_views.profile, name='profile'),
    path('profile/edit/<int:pk>/',
         user_views.ProfileUpdateStatus.as_view(),
         name='profile-update'),
    path('user/<int:pk>/',
         user_views.UserUpdateView.as_view(),
         name='user-update'),
    path('follow/<int:pk>/', user_views.follow_view, name='follow-user'),
    path('unfollow/<int:pk>/', user_views.unfollow_view, name='unfollow-user'),
]

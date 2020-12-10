from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from . import views

urlpatterns = [
    path('', views.allPosts, name='allPosts'),
    path('followingPosts', views.followingPosts, name='followingPosts'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='photogram/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='photogram/logout.html'), name='logout'),
    path('createpost', views.createPost, name='createPost'),
    path('profileedit/', views.profileEdit, name='profileEdit'),
    re_path(r'^profile/(?P<username>[\w ]+)/$', views.profile, name="profile"),
    path("likePost/<int:postid>", views.likePost, name="likePost"),
    re_path(r'^follow/(?P<username>[\w ]+)/$', views.follow, name="follow"),
    path("comment/<int:postId>", views.comments, name="comment"),
]
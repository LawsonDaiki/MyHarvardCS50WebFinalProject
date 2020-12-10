from django.contrib import admin
from .models import Profile, Post, Likes, Following, Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Following)
admin.site.register(Comment)

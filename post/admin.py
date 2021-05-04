from django.contrib import admin

# Register your models here.
from post.models import Post, Like, Follow, Comment

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Comment)


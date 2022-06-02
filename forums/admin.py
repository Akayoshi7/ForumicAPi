from django.contrib import admin
from forums.models import Post, Category, Comment, Rating

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Rating)
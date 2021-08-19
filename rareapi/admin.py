from django.contrib import admin
from rareapi.models import RareUser, Post, Comment, Category
from rareapi.models.rare_users import RareUser

# Register your models here.
admin.site.register(RareUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)

from django.contrib import admin
from userprofile.models import UserProfile
from blog.models import Category, Post

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post)
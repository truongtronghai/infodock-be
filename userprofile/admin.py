from django.contrib import admin

from blog.models import Category, Post
from userprofile.models import UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)

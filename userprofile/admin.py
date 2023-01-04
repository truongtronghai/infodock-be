from django.contrib import admin
from userprofile.models import UserProfile
from blog.models import Category, Post

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","slug","parent")

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
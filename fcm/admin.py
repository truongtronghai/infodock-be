from django.contrib import admin

from .models import FcmRegistrationId


# Register your models here.
class FcmRegistrationIdAdmin(admin.ModelAdmin):
    list_display = ("user", "deviceType", "registrationId")


admin.site.register(FcmRegistrationId, FcmRegistrationIdAdmin)

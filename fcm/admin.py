from django.contrib import admin

from .models import FcmRegistrationId


# Register your models here.
class FcmRegistrationIdAdmin(admin.ModelAdmin):
    list_display = ("user", "deviceType", "registrationId")
    # disabled Delete button in admin section of this model
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(FcmRegistrationId, FcmRegistrationIdAdmin)

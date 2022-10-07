from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# CREDIT: Pyplane
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUserAdmin(UserAdmin):
    """Set additional fieldset to display on the change user page of the admin
    portal.
    """

    model = CustomUser

    fieldsets = (
        *UserAdmin.fieldsets,
        ("Seller Status", {"fields": ("is_seller",)}),
    )

    list_display = (
        "username",
        "id",
        "is_staff",
        "is_seller",
    )

    ordering = ("id",)


# register models with admin site so they can be managed
admin.site.register(CustomUser, CustomUserAdmin)

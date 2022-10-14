from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Profile


class CustomProfileAdmin(ModelAdmin):
    """Customize admin list view fields."""

    model = Profile

    list_display = ("id", "__str__", "owner_id", "owner")

    ordering = ("id",)


admin.site.register(Profile, CustomProfileAdmin)

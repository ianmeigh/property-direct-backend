from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Follower


class CustomFollowerAdmin(ModelAdmin):
    """Customize admin list view fields."""

    model = Follower

    list_display = ("id", "owner", "followed")

    ordering = ("id",)


admin.site.register(Follower, CustomFollowerAdmin)

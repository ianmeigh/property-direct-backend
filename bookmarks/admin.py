from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Bookmark


class CustomBookmarkAdmin(ModelAdmin):
    """Customize admin list view fields."""

    model = Bookmark

    list_display = ("id", "owner", "property")

    ordering = ("id",)


admin.site.register(Bookmark, CustomBookmarkAdmin)

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Note


class CustomNoteAdmin(ModelAdmin):
    """Customize admin list view fields."""

    model = Note

    list_display = ("id", "owner", "property", "content")

    ordering = ("id",)


admin.site.register(Note, CustomNoteAdmin)

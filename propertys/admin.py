from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Property


class CustomPropertyAdmin(ModelAdmin):
    """Customize admin list view fields."""

    model = Property

    list_display = ("id", "owner", "__str__")

    ordering = ("id",)


admin.site.register(Property, CustomPropertyAdmin)

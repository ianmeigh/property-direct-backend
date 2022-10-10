from django.db import IntegrityError
from rest_framework import serializers

from .models import Bookmark


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL: https://github.com/Code-Institute-Solutions/drf-api
class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark Serializer

    Used with list and detail view.
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Bookmark
        fields = [
            "id",
            "owner",
            "property",
            "created_at",
        ]

    def create(self, validated_data):
        """Handle integrity errors caused if User tries to bookmark a property
        more than once.
        """

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "possible duplicate"})

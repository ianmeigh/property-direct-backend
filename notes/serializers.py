from rest_framework import serializers

from .models import Note


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL:    https://github.com/Code-Institute-Solutions/drf-api
class NoteSerializer(serializers.ModelSerializer):
    """Note Serializer

    Used with list view.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    class Meta:
        model = Note
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "property",
            "content",
            "created_at",
            "updated_at",
        ]


class NoteDetailSerializer(NoteSerializer):
    """Note Detail Serializer

    Used with detail view.
    """

    property = serializers.ReadOnlyField(source="property.id")

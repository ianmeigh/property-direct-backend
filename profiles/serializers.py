from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer used for anonymous user requests.

    Hide contact information.
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "image",
            "created_at",
            "updated_at",
        ]


class ProfileSerializerAuthenticated(ProfileSerializer):
    """Serializer used for authenticated user requests.

    Display contact information.
    """

    class Meta:
        model = Profile
        fields = ProfileSerializer.Meta.fields + [
            "email",
            "telephone_landline",
            "telephone_mobile",
        ]

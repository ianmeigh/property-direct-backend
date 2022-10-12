from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL: https://github.com/Code-Institute-Solutions/drf-api
class CurrentUserSerializer(UserDetailsSerializer):
    """Add user and profile details to the information returned when requesting
    logged in user details."""

    profile_id = serializers.ReadOnlyField(source="profile.id")
    profile_image = serializers.ReadOnlyField(source="profile.image.url")

    # Add 'is_seller' to the returned information
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "profile_id",
            "profile_image",
            "is_seller",
        )

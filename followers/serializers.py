from django.db import IntegrityError
from rest_framework import serializers

from .models import Follower


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL:    https://github.com/Code-Institute-Solutions/drf-api
class FollowerSerializer(serializers.ModelSerializer):
    """Follower Serializer

    Used with list and detail view.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    followed_name = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follower
        fields = [
            "id",
            "owner",
            "followed",
            "followed_name",
            "created_at",
        ]

    def create(self, validated_data):
        """Manage object creation

        - Ensure a User cannot follow themselves
        - Ensure only Seller can be followed
        - Handle integrity errors caused if User tries to follow another User
        more than once.
        """
        if validated_data["owner"] == validated_data["followed"]:
            raise serializers.ValidationError(
                {"detail": "can't follow yourself"}
            )
        elif validated_data["followed"].get_is_seller() is False:
            raise serializers.ValidationError(
                {"detail": "can't follow a user that isn't a seller"}
            )
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "possible duplicate"})

import re

from followers.models import Follower
from property_direct_api.utils import validate_image_util
from rest_framework import serializers

from .models import Profile


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL:    https://github.com/Code-Institute-Solutions/drf-api
class ProfileSerializer(serializers.ModelSerializer):
    """Serializer used for anonymous user requests.

    Hide contact information.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    property_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_seller = serializers.ReadOnlyField(source="owner.is_seller")

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.owner

    def get_following_id(self, obj):
        """Returns the id of the follower object, for each Profile being
        followed by currently authenticated User.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def validate_image(self, value):
        valid_image = validate_image_util(value)
        return valid_image

    def validate_email(self, value):
        # CREDIT: Basic regular expression for email address
        # AUTHOR: Róbert Papp
        # URL:    https://emailregex.com/ - http://disq.us/p/10frbr8
        pattern = r"\S+@\S+\.\S+"

        # TODO: MailGun Email Validation
        if re.match(pattern, value):
            return value
        raise serializers.ValidationError(
            "Please enter a valid email address."
        )

    def validate_telephone_mobile(self, value):
        # CREDIT: Regular expression for UK mobile number adapted from this
        #         source
        # AUTHOR: BlackVegetable
        # URL:    https://stackoverflow.com/a/16405304
        pattern = r"^(07[\d]{9})$"

        if re.match(pattern, value):
            return value
        raise serializers.ValidationError(
            "Please enter a valid UK (11-digit) mobile number, starting with "
            "zero, excluding +44, with no spaces."
        )

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "is_owner",
            "name",
            "description",
            "image",
            "following_id",
            "property_count",
            "followers_count",
            "following_count",
            "is_seller",
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

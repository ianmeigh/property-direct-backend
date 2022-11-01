from bookmarks.models import Bookmark
from haversine import Unit, haversine
from property_direct_api.exceptions import (
    ExternalAPIUnavailable,
    PostCodeInvalid,
)
from property_direct_api.utils import validate_image_util
from rest_framework import serializers

from .models import Property
from .utils import get_postcode_details


class PropertySerializer(serializers.ModelSerializer):
    """Property Serializer.

    Used with list view, as distance calculation (performed in
    PropertySearchSerializer) only required for search results.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    profile_telephone_mobile = serializers.ReadOnlyField(
        source="owner.profile.telephone_mobile"
    )
    profile_telephone_landline = serializers.ReadOnlyField(
        source="owner.profile.telephone_landline"
    )
    profile_email = serializers.ReadOnlyField(source="owner.profile.email")
    bookmark_id = serializers.SerializerMethodField()
    bookmarks_count = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    def get_bookmark_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            bookmark = Bookmark.objects.filter(
                owner=user, property=obj
            ).first()
            return bookmark.id if bookmark else None
        return None

    def validate_image_hero(self, value):
        valid_image = validate_image_util(value)
        return valid_image

    def validate_floorplan(self, value):
        valid_image = validate_image_util(value)
        return valid_image

    def validate_epc(self, value):
        valid_image = validate_image_util(value)
        return valid_image

    def validate_postcode(self, value):
        try:
            get_postcode_details(value)
        except PostCodeInvalid:
            raise serializers.ValidationError(
                "Please enter a valid UK postcode"
            )
        except ExternalAPIUnavailable:
            raise serializers.ValidationError(
                "Postcode verification service temporarily unavailable, "
                "please report this and try again later."
            )
        return value.lower()

    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "property_name",
            "profile_telephone_mobile",
            "profile_telephone_landline",
            "profile_email",
            "property_number",
            "street_name",
            "locality",
            "city",
            "postcode",
            "description",
            "price",
            "image_hero",
            "floorplan",
            "epc",
            "property_type",
            "tenure",
            "council_tax_band",
            "num_bedrooms",
            "num_bathrooms",
            "has_garden",
            "has_parking",
            "is_sold_stc",
            "latitude",
            "longitude",
            "bookmark_id",
            "bookmarks_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("longitude", "latitude")


class PropertySearchSerializer(PropertySerializer):
    """Property Search Serializer.

    Used with list view when a postcode is provided as a query parameter. Uses
    the longitude and latitude of 2 points to calculate the distance between
    them and adds this to the serialized data.
    """

    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        """Calculate the distance between 2 points (using longitude and
        latitude)

        Make use of the Haversine Formula as implemented in the package
        "haversine" (https://github.com/mapado/haversine).
        """
        # Try / Except Block used defensively in the event a future maintainer
        # calls the search serializer without also passing point of origin
        # information to the serializer context.
        try:
            point_of_origin_coords = (
                self.context["point_of_origin_lon"],
                self.context["point_of_origin_lat"],
            )

            property_coords = (obj.longitude, obj.latitude)

            distance = haversine(
                point_of_origin_coords, property_coords, unit=Unit.MILES
            )
        except KeyError:
            return None
        return distance

    class Meta:
        model = Property
        fields = PropertySerializer.Meta.fields + [
            "distance",
        ]

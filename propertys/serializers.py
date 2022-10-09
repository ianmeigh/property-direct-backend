from rest_framework import serializers

from .models import Property
from .utils import validate_property_image


class PropertySerializer(serializers.ModelSerializer):
    """Property Serializer."""

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    longitude = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    def validate_image_hero(self, value):
        valid_image = validate_property_image(value)
        return valid_image

    def validate_floorplan(self, value):
        valid_image = validate_property_image(value)
        return valid_image

    def validate_epc(self, value):
        valid_image = validate_property_image(value)
        return valid_image

    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "property_name",
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("longitude", "latitude")

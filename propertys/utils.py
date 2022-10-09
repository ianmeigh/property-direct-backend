import requests
from property_direct_api.exceptions import (
    ExternalAPIUnavailable,
    PostCodeInvalid,
)
from rest_framework import serializers


# CREDIT: Validation logic adapted from the Code Institute DRF Tutorial Project
# URL: https://github.com/Code-Institute-Solutions/drf-api
def validate_property_image(file_obj):
    """Validate Image File based on height, width and file size."""
    max_image_width = 4096
    max_image_height = 4096
    maximum_file_size = 2  # File size unit is MB

    if file_obj.size > (1024 * 1024 * maximum_file_size):
        raise serializers.ValidationError(
            "Image size should be smaller than 2MB."
        )
    if file_obj.image.width > max_image_width:
        raise serializers.ValidationError(
            f"Image width should be less than {max_image_width}px."
        )
    if file_obj.image.width > max_image_height:
        raise serializers.ValidationError(
            f"Image height should be less than {max_image_height}px."
        )
    return file_obj


def get_postcode_details(postcode):
    """Fetches postcode information from external API (e.g. Longitude,
    Latitude).

    - External API used as validation method for user defined postcode as it
      raises custom exceptions.
    - External API URL: https://api.postcodes.io/
    """
    api_response = requests.get(
        f"https://api.postcodes.io/postcodes/{postcode}"
    )
    response_obj = api_response.json()

    if response_obj["status"] == 200:
        return response_obj["result"]
    if response_obj["status"] == 404 and (
        response_obj["error"] == "Postcode not found"
        or response_obj["error"] == "Invalid postcode"
    ):
        raise PostCodeInvalid
    elif (
        response_obj["status"] == 404
        and response_obj["error"] == "Resource not found"
    ):
        raise ExternalAPIUnavailable

    return response_obj

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

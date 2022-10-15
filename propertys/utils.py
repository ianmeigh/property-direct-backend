import requests
from property_direct_api.exceptions import (
    ExternalAPIUnavailable,
    PostCodeInvalid,
    RadiusInvalid,
)


def get_postcode_details(postcode):
    """Fetches postcode information from external API (e.g. Longitude,
    Latitude).

    - External API URL: https://api.postcodes.io/.

    Args:
        postcode (string): Postcode information.

    Raises:
        PostCodeInvalid: Raised when postcode invalid.
        ExternalAPIUnavailable: Raised when external API unavailable.

    Returns:
        dict: Postcode information from external API.
    """
    api_response = requests.get(
        f"https://api.postcodes.io/postcodes/{postcode}"
    )
    response_obj = api_response.json()

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

    return response_obj["result"]


def convert_radius_to_float(input_string):
    """Type casts input string to a float.

    Args:
        input_string (string): Input parameter.

    Raises:
        RadiusInvalid: Custom API Exception.

    Returns:
        float: Explicitly converted input.
    """
    try:
        radius_float = round(float(input_string), 1)
    except ValueError:
        raise RadiusInvalid
    return radius_float

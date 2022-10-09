from rest_framework.exceptions import APIException


class ExternalAPIUnavailable(APIException):
    status_code = 503
    default_detail = {
        "error": [
            "Postcode verification service temporarily unavailable, "
            "please report this and try again later."
        ]
    }
    default_code = "service_unavailable"


class PostCodeInvalid(APIException):
    status_code = 400
    default_detail = {"error": ["Postcode not valid"]}
    default_code = "postcode_invalid"
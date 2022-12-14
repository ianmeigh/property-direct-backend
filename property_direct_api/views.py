from rest_framework.decorators import api_view
from rest_framework.response import Response

from .settings import (
    JWT_AUTH_COOKIE,
    JWT_AUTH_REFRESH_COOKIE,
    JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)


@api_view()
def root_route(request):
    return Response(
        {
            "message": "Welcome to the Property Direct API",
            "documentation": "https://github.com/ianmeigh/property-direct-"
            "backend",
        }
    )


# CREDIT: Code from Code Institute DRF Tutorial Project - dj-rest-auth logout
#         view fix
# URL:    https://github.com/Code-Institute-Solutions/drf-api
@api_view(["POST"])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value="",
        httponly=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value="",
        httponly=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response

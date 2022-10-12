from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from rest_framework import serializers


# CREDIT: Adapted from - Registration and Authentication in Django apps with
#         dj-rest-auth
# AUTHOR: Bruno Michetti
# URL:    https://www.rootstrap.com/blog/registration-and-authentication-in-dja
#         ngo-apps-with-dj-rest-auth/
class CustomRegisterSerializer(RegisterSerializer):
    """Add 'is_seller' and remove 'email' from dj_rest_auth registration view
    and save added value on successful registration."""

    is_seller = serializers.BooleanField(default=False)
    email = None

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.is_seller = self.data.get("is_seller")
        user.save()
        return user

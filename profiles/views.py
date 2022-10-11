from django.db.models import Count
from property_direct_api.permissions import (
    IsProfileOwnerOrViewingSellerProfile,
)
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from .models import Profile
from .serializers import ProfileSerializer, ProfileSerializerAuthenticated


class ProfileListView(ListAPIView):
    """Profile List View

    - Only display seller profiles to keep standard user profiles private.
    - Return different Serializer content based on authentication state.
    """

    queryset = (
        Profile.objects.all()
        .filter(owner__is_seller=True)
        .annotate(
            property_count=Count("owner__property", distinct=True),
            followers_count=Count("owner__followed", distinct=True),
            following_count=Count("owner__following", distinct=True),
        )
        .order_by("-created_at")
    )
    filter_backends = [OrderingFilter]
    ordering_fields = [
        "property_count",
        "followers_count",
        "following_count",
    ]

    def get_serializer_class(self):
        """Return different serializers based on authentication status

        Authenticated users are able to see profile contact information.
        """
        if self.request.user.is_authenticated:
            return ProfileSerializerAuthenticated
        else:
            return ProfileSerializer


class ProfileDetailView(RetrieveUpdateAPIView):
    """Profile Detail (Retrieve and Update) View

    - Custom permissions class to control profile privacy (and permissions).
    - Return different Serializer content based on authentication state.
    """

    queryset = Profile.objects.annotate(
        property_count=Count("owner__property", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    permission_classes = [IsProfileOwnerOrViewingSellerProfile]

    def get_serializer_class(self):
        """Return different serializers based on authentication status.

        Authenticated users are able to see profile contact information.
        """
        if self.request.user.is_authenticated:
            return ProfileSerializerAuthenticated
        else:
            return ProfileSerializer

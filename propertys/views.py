from property_direct_api.permissions import IsOwnerOrReadOnly, IsSeller
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Property
from .serializers import PropertySerializer
from .utils import get_postcode_details


class PropertyListView(ListAPIView):
    """Property List View"""

    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyCreateView(CreateAPIView):
    """Property Create View

    Custom permissions class to restrict property creation (to only Sellers).
    """

    serializer_class = PropertySerializer
    permission_classes = [IsSeller]
    queryset = Property.objects.all()

    def perform_create(self, serializer):
        """Add extra information before the object is saved (created).

        - Retrieve and add the Longitude and Latitude information for the
          postcode.
        - Add an owner before the model object is created.
        """
        postcode = serializer.validated_data["postcode"]
        postcode_details = get_postcode_details(postcode)
        latitude = postcode_details["latitude"]
        longitude = postcode_details["longitude"]
        serializer.save(
            owner=self.request.user, latitude=latitude, longitude=longitude
        )


class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    """Property Detail (Retrieve, Update and Destroy) View"""

    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Property.objects.all()

    def perform_update(self, serializer):
        """Add extra information before the object is saved (updated).

        - Retrieves the Longitude and Latitude information if the
          postcode has been updated.
        """
        # Get the postcode from the serializer
        updated_postcode = serializer.validated_data["postcode"]

        # Get the existing property object
        obj = serializer.instance

        # If the postcode from the serializer doesn't match doesn't match the
        # property objects current postcode, a change has been made and the
        # longitude and latitude should be updated.
        if updated_postcode != obj.postcode:
            result = get_postcode_details(updated_postcode)
            obj.latitude = result["latitude"]
            obj.longitude = result["longitude"]
        serializer.save()

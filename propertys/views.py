from math import cos, pi

from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from property_direct_api.permissions import IsOwnerOrReadOnly, IsSeller
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .filters import CustomPropertyFilters
from .models import Property
from .serializers import PropertySearchSerializer, PropertySerializer
from .utils import convert_radius_to_float, get_postcode_details


class PropertyListView(ListAPIView):
    """Property List View"""

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = [
        "bookmarks_count",
        "bookmarks__created_at",
    ]
    filterset_class = CustomPropertyFilters

    # Class variables to hold query information
    search_point_of_origin_lat = ""
    search_point_of_origin_lon = ""
    query_param_postcode = ""
    query_param_radius = ""
    postcode = ""

    def initial(self, request, *args, **kwargs):
        """Performs initial checks for search functionality

        - Checks for query parameters of 'postcode' and 'radius'.
        - If 'postcode' query parameter is populated, validate and geocode
        - If 'radius' is present, convert to float to validate, otherwise set
          to 0.5
        """
        # Set Class instance variables with query parameters or fallback
        # values
        self.query_param_postcode = self.request.query_params.get(
            "postcode", ""
        )
        self.query_param_radius = self.request.query_params.get("radius", "")

        # Validate and Geocode Postcode
        if self.query_param_postcode:
            query_postcode_details = get_postcode_details(
                self.query_param_postcode
            )
            self.search_point_of_origin_lat = query_postcode_details[
                "latitude"
            ]
            self.search_point_of_origin_lon = query_postcode_details[
                "longitude"
            ]
        # Validate or Set Radius
        if self.query_param_radius:
            self.query_param_radius = convert_radius_to_float(
                self.query_param_radius
            )
        else:
            self.query_param_radius = 0.5
        return super().initial(request, *args, **kwargs)

    def get_queryset(self):
        """Filters the queryset using a bounding box

        If a 'postcode' and 'radius' are supplied as query parameters, the
        minimum and maximum longitude and latitude are calculated to form a
        bounding box. This is then used to filter property objects and form the
        queryset.
        """

        if self.query_param_postcode:
            # CREDIT: Adapted from "Selecting points within a bounding
            #         circle"
            # AUTHOR: Chris Veness
            # URL:    https://www.movable-type.co.uk/scripts/latlong-db.html

            R = 3958.8  # Earth's mean radius in Miles

            search_area_min_lat = self.search_point_of_origin_lat - (
                self.query_param_radius / R * 180 / pi
            )
            search_area_max_lat = self.search_point_of_origin_lat + (
                self.query_param_radius / R * 180 / pi
            )
            search_area_min_lon = self.search_point_of_origin_lon - (
                self.query_param_radius
                / R
                * 180
                / pi
                / cos(self.search_point_of_origin_lat * pi / 180)
            )
            search_area_max_lon = self.search_point_of_origin_lon + (
                self.query_param_radius
                / R
                * 180
                / pi
                / cos(self.search_point_of_origin_lat * pi / 180)
            )

            queryset = (
                Property.objects.filter(
                    latitude__gte=search_area_min_lat,
                    latitude__lte=search_area_max_lat,
                    longitude__gte=search_area_min_lon,
                    longitude__lte=search_area_max_lon,
                )
                .annotate(
                    bookmarks_count=Count("bookmarks", distinct=True),
                )
                .order_by("-created_at")
            )
        else:
            queryset = Property.objects.annotate(
                bookmarks_count=Count("bookmarks", distinct=True),
            ).order_by("-created_at")
        return queryset

    # CREDIT: Adapted from Pass extra arguments to Serializer Class in Django
    #         Rest Framework.
    # AUTHOR: M.Void - StackOverflow
    # URL:    https://stackoverflow.com/a/38723709
    def get_serializer_context(self):
        """Update the context passed to the serializer.

        Include the longitude and latitude of the search's point of origin
        (POO), so the distance from the POO can be calculated for each object
        in the serializer.
        """
        context = super(PropertyListView, self).get_serializer_context()
        if self.query_param_postcode:
            context["point_of_origin_lat"] = self.search_point_of_origin_lat
            context["point_of_origin_lon"] = self.search_point_of_origin_lon
        return context

    def get_serializer_class(self, *args, **kwargs):
        """Return serializer class to be used.

        If query parameters exist for an area search, then use the serializer
        that calculates distance from the search's point of origin.
        """
        if bool(self.query_param_postcode):
            serializer_class = PropertySearchSerializer  # inc distance
        else:
            serializer_class = PropertySerializer  # no distance
        return serializer_class


class PropertyCreateView(CreateAPIView):
    """Property Create View

    - Custom permissions class to restrict property creation (to only Sellers).
    - Return different Serializer content based on query parameters.
    """

    serializer_class = PropertySerializer
    permission_classes = [IsSeller]
    queryset = Property.objects.all()

    def perform_create(self, serializer):
        """Add extra information before the object is saved (created).

        - Fetch postcode information and add the Longitude and Latitude
          of the postcode before the model object is created.
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
    """Property Detail (Retrieve, Update and Destroy) View

    - Retrieve a property by id and allow the owner to update or delete the
      object.
    """

    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Property.objects.all()

    def perform_update(self, serializer):
        """Add extra information before the object is saved (updated).

        - Fetch postcode information and add the Longitude and Latitude of the
          postcode to the model object instance, if the postcode has been
          updated.
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

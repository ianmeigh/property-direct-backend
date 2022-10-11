from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Property


class CustomPropertyFilters(filters.FilterSet):
    """Custom Property FilterSet

    - property_feed_for_profile - Properties listed by users the currently
      authenticated user has followed.
    - bookmarked_properties_for_profile - Properties bookmarked by the
      currently authenticated user.
    - properties_listed_by_profile - Property listings owned by the currently
      authenticated user.
    - price - Price Range (price_min=, price_max=)
    - bedrooms - Number of Bedrooms (bedrooms_min=, bedrooms_max=)
    - bathrooms - Number of Bathrooms (bedrooms_min=, bedrooms_max=)
    - has_garden - Property has a Garden (true or false)
    - has_parking - Property has Parking (true or false)
    - is_sold_stc - Property is Sold Subject to Contract (true or false)
    """

    # Properties listed by users the currently authenticated user has followed.
    property_feed_for_profile = filters.ChoiceFilter(
        label="Property feed for User (Profile)",
        choices=get_user_model()
        .objects.all()
        .values_list("profile__id", "profile__owner__username"),
        field_name="owner__followed__owner__profile",
    )

    # Properties bookmarked by the currently authenticated user.
    bookmarked_properties_for_profile = filters.ChoiceFilter(
        label="Properties Bookmarked by User (Profile)",
        choices=get_user_model()
        .objects.all()
        .values_list("profile__id", "profile__owner__username"),
        field_name="bookmarks__owner__profile",
    )
    # Property listings owned by the currently authenticated user.
    properties_listed_by_profile = filters.ChoiceFilter(
        label="Properties owned by User (Profile)",
        choices=get_user_model()
        .objects.all()
        .values_list("profile__id", "profile__owner__username"),
        field_name="owner__profile",
    )
    property_type = filters.ChoiceFilter(
        choices=Property.property_type_choices
    )
    price = filters.RangeFilter(field_name="price")
    bedrooms = filters.RangeFilter(field_name="num_bedrooms")
    bathrooms = filters.RangeFilter(field_name="num_bathrooms")
    has_garden = filters.BooleanFilter(field_name="has_garden")
    has_parking = filters.BooleanFilter(field_name="has_parking")
    is_sold_stc = filters.BooleanFilter(field_name="is_sold_stc")

    class Meta:
        model = Property
        fields = [
            "property_feed_for_profile",
            "bookmarked_properties_for_profile",
            "properties_listed_by_profile",
            "property_type",
            "price",
            "bedrooms",
            "bathrooms",
            "has_garden",
            "has_parking",
            "is_sold_stc",
        ]

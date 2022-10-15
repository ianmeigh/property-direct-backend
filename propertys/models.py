from django.conf import settings
from django.db import models


class Property(models.Model):
    """Property Model.

    Holds information about properties for sale.
    """

    property_type_choices = [
        ("apartment", "Apartment"),
        ("detached", "Detached"),
        ("semi-detached", "Semi-detached"),
        ("terraced", "Terraced"),
        ("end terrace", "End Terrace"),
        ("cottage", "Cottage"),
        ("bungalows", "Bungalows"),
    ]

    tenure_choices = [
        ("", "I don't know"),
        ("freehold", "Freehold"),
        ("shared freehold", "Shared freehold"),
        ("leasehold", "Leasehold"),
        ("commonhold", "Commonhold"),
        ("shared ownership", "Shared ownership"),
    ]

    council_tax_band_choices = [
        ("", "I don't know"),
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
        ("e", "E"),
        ("f", "F"),
        ("g", "G"),
        ("h", "H"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    property_name = models.CharField(max_length=35, null=True, blank=True)
    property_number = models.PositiveIntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=35)
    locality = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    postcode = models.CharField(max_length=8)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image_hero = models.ImageField(
        upload_to="images/",
        default="../default_property_image_lwan0m.jpg",
        blank=True,
    )
    floorplan = models.ImageField(upload_to="images/", blank=True)
    epc = models.ImageField(upload_to="images/", blank=True)
    property_type = models.CharField(
        max_length=13, choices=property_type_choices
    )
    tenure = models.CharField(
        max_length=16, choices=tenure_choices, blank=True
    )
    council_tax_band = models.CharField(
        max_length=1, choices=council_tax_band_choices, blank=True
    )
    num_bedrooms = models.PositiveIntegerField(blank=False)
    num_bathrooms = models.PositiveIntegerField(blank=False)
    has_garden = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    is_sold_stc = models.BooleanField(default=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.street_name, self.locality, self.city, self.postcode}"

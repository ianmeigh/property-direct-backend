from django.conf import settings
from django.db import models


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL:    https://github.com/Code-Institute-Solutions/drf-api
class Profile(models.Model):
    """Profile model.

    Linked to the CustomUser model.
    """

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.TextField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    email = models.CharField(max_length=50, blank=True)
    telephone_landline = models.CharField(max_length=11, blank=True)
    telephone_mobile = models.CharField(max_length=11, blank=True)
    image = models.ImageField(
        upload_to="images/", default="../default_profile_hthtjb.jpg"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner}'s profile"

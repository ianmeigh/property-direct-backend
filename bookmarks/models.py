from django.conf import settings
from django.db import models
from propertys.models import Property


# CREDIT: Class from Code Institute DRF Tutorial Project with minor adaptations
# URL: https://github.com/Code-Institute-Solutions/drf-api
class Bookmark(models.Model):
    """Bookmark model.

    - Related to 'owner' (User model instance) and 'property' (Property model
      instance).
    - Property cannot be bookmarked more than once ('unique_together' in Meta
      class).
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["owner", "property"]

    def __str__(self):
        return f"{self.owner, self.property}"

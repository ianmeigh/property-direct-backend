from django.conf import settings
from django.db import models


# CREDIT: Class from Code Institute DRF Tutorial Project with minor adaptations
# URL: https://github.com/Code-Institute-Solutions/drf-api
class Follower(models.Model):
    """Follower Model.

    - Related to 'owner' and 'followed' (both User model
      instances).
    - 'owner' is a User that is following a User.
    - 'followed' is a User that is followed by 'owner'.
    - Users cannot be followed more than once ('unique_together' in Meta
      class).
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["owner", "followed"]

    def __str__(self):
        return f"{self.owner.username, self.followed.username}"

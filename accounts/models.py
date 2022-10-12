from django.contrib.auth.models import AbstractUser
from django.db import models


# CREDIT: Adapted from Pyplane and Django Documentation
# URL:    https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUser(AbstractUser):
    """Custom User Model created by extending AbstractUser

    User accounts have the additional field 'is_seller'. This field determines
    the role of the users account:

    Seller          - Can create property listings
    Standard User   - Can browse property listings
    """

    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_is_seller(self):
        return self.is_seller

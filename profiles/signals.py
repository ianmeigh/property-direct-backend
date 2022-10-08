from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    """Signal to create a Profile object when a User object is created."""
    if created:
        Profile.objects.create(owner=instance)

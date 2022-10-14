from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from profiles.models import Profile


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, *args, **kwargs):
    """Signal to delete a User object when a Profile object is deleted."""
    user = get_user_model().objects.get(pk=instance.owner_id)
    user.delete()

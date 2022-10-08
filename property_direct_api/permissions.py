from rest_framework import permissions


# CREDIT: IsOwnerOrReadOnly Permission Class from the Code Institute DRF
# Tutorial Project
# URL: https://github.com/Code-Institute-Solutions/drf-api
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwnerOrViewingSeller(permissions.BasePermission):
    """Custom permissions to determine profile retrieve and update behavior.

    - Non-Seller users profiles are private and won't be visible on 'GET'
      requests.
    - Seller profiles are public (except contact information) and will be
      visible.
    - Profiles owners will be able to view and edit their own profile.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.owner.is_seller:
            return True
        return obj.owner == request.user

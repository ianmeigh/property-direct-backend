from property_direct_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from .models import Follower
from .serializers import FollowerSerializer


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL: https://github.com/Code-Institute-Solutions/drf-api
class FollowerListView(ListCreateAPIView):
    """Follower List/Create View

    - Only display following information to their owners to keep following
      activity private.
    - Create a follower if authenticated.
    """

    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter the queryset to display only bookmarks owned by the currently
        authenticated User, to keep bookmarks private.
        """
        current_user = self.request.user
        if current_user.is_anonymous:
            queryset = Follower.objects.none()
        else:
            queryset = Follower.objects.filter(owner=current_user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetailView(RetrieveDestroyAPIView):
    """Follower Detail (Retrieve, Update and Destroy) View

    - Retrieve a Follower object by id and allow the owner to view or delete
      the object.
    """

    serializer_class = FollowerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Filter the queryset to display only bookmarks owned by the currently
        authenticated User, to keep bookmarks private.
        """
        current_user = self.request.user
        if current_user.is_anonymous:
            queryset = Follower.objects.none()
        else:
            queryset = Follower.objects.filter(owner=current_user)
        return queryset

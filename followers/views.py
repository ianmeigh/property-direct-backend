from property_direct_api.mixins import IsOwnerQuerysetFilter
from property_direct_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from .models import Follower
from .serializers import FollowerSerializer


# CREDIT: Adapted from the Code Institute DRF Tutorial Project
# URL:    https://github.com/Code-Institute-Solutions/drf-api
class FollowerListView(IsOwnerQuerysetFilter, ListCreateAPIView):
    """Follower List/Create View

    - Use IsOwnerQuerysetFilter Mixin to only display following information to
      their owners to keep following activity private.
    - Create a follower if authenticated.
    """

    model = Follower
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetailView(IsOwnerQuerysetFilter, RetrieveDestroyAPIView):
    """Follower Detail (Retrieve, Update and Destroy) View

    - Retrieve a Follower object by id and allow the owner to view and delete
      the object.
    - Use IsOwnerQuerysetFilter Mixin to only display following information to
    their owners to keep following activity private.
    """

    model = Follower
    serializer_class = FollowerSerializer
    permission_classes = [IsOwnerOrReadOnly]

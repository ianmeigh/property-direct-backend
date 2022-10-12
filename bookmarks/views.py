from property_direct_api.mixins import IsOwnerQuerysetFilter
from property_direct_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkListView(IsOwnerQuerysetFilter, ListCreateAPIView):
    """Bookmark List/Create View.

    - List or Create a bookmark (latter if authenticated).
    - Use IsOwnerQuerysetFilter Mixin to only display bookmarks to their owners
      to keep bookmarks private.
    - Create a bookmark if authenticated.
    """

    model = Bookmark
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookmarkDetailView(IsOwnerQuerysetFilter, RetrieveDestroyAPIView):
    """Bookmark Detail (Retrieve, Update and Destroy) View

    - Retrieve a Bookmark by id and allow the owner to view and delete the
    object.
    - Use IsOwnerQuerysetFilter Mixin to only display bookmarks to their owners
      to keep bookmarks private.
    """

    model = Bookmark
    serializer_class = BookmarkSerializer
    permission_classes = [IsOwnerOrReadOnly]

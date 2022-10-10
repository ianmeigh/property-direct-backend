from property_direct_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkListView(ListCreateAPIView):
    """Bookmark List/Create View.

    - List or Create a bookmark (latter if authenticated).
    - Only display bookmarks to their owners to keep bookmarks private.
    """

    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter the queryset to display only bookmarks owned by the currently
        authenticated User, to keep bookmarks private.
        """
        current_user = self.request.user
        if current_user.is_anonymous:
            queryset = Bookmark.objects.none()
        else:
            queryset = Bookmark.objects.filter(owner=current_user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookmarkDetailView(RetrieveUpdateDestroyAPIView):
    """Bookmark Detail (Retrieve, Update and Destroy) View

    - Retrieve a Bookmark by id and allow the owner to update or delete the
    object.
    """

    serializer_class = BookmarkSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Filter the queryset to display only bookmarks owned by the currently
        authenticated User, to keep bookmarks private.
        """
        current_user = self.request.user
        if current_user.is_anonymous:
            queryset = Bookmark.objects.none()
        else:
            queryset = Bookmark.objects.filter(owner=current_user)
        return queryset

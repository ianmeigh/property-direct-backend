from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

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

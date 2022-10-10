from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from .models import Follower
from .serializers import FollowerSerializer


# CREDIT: Class from Code Institute DRF Tutorial Project with minor adaptations
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

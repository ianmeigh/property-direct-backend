from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from .models import Note
from .serializers import NoteSerializer


class NoteListView(ListCreateAPIView):
    """Note List/Create View

    - Only display notes to their owners to keep notes private.
    """

    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter the queryset to display only notes owner by the currently
        authenticated User, to keep notes private.
        """
        current_user = self.request.user
        if current_user.is_anonymous:
            queryset = Note.objects.none()
        else:
            queryset = Note.objects.filter(owner=current_user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

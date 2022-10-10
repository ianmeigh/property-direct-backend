from property_direct_api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Note
from .serializers import NoteDetailSerializer, NoteSerializer


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


class NoteDetailView(RetrieveUpdateDestroyAPIView):
    """Note Detail (Retrieve, Update and Destroy) View

    - Retrieve a Note by id and allow the owner to update or delete the
    object.
    """

    serializer_class = NoteDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

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

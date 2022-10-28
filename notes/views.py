from django_filters.rest_framework import DjangoFilterBackend
from property_direct_api.mixins import IsOwnerQuerysetFilter
from property_direct_api.permissions import (
    AnonSafeMethodsOnly,
    IsOwnerOrReadOnly,
)
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Note
from .serializers import NoteDetailSerializer, NoteSerializer


class NoteListView(IsOwnerQuerysetFilter, ListCreateAPIView):
    """Note List/Create View

    - Use IsOwnerQuerysetFilter Mixin to only display notes to their owners
      to keep notes private.
    - Create a note if authenticated.
    """

    model = Note
    serializer_class = NoteSerializer
    permission_classes = [AnonSafeMethodsOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["property"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetailView(IsOwnerQuerysetFilter, RetrieveUpdateDestroyAPIView):
    """Note Detail (Retrieve, Update and Destroy) View

    - Retrieve a Note by id and allow the owner to update or delete the
      object.
    - Use IsOwnerQuerysetFilter Mixin to only display notes to their owners
      to keep notes private.
    """

    model = Note
    serializer_class = NoteDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

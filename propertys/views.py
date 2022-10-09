from property_direct_api.permissions import IsOwnerOrReadOnly, IsSeller
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Property
from .serializers import PropertySerializer


class PropertyListView(ListAPIView):
    """Property List View"""

    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyCreateView(CreateAPIView):
    """Property Create View

    Custom permissions class to restrict property creation (to only Sellers).
    """

    serializer_class = PropertySerializer
    permission_classes = [IsSeller]
    queryset = Property.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetailView(RetrieveUpdateDestroyAPIView):
    """Property Detail (Retrieve, Update and Destroy) View"""

    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Property.objects.all()

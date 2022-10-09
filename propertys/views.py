from rest_framework.generics import ListAPIView

from .models import Property
from .serializers import PropertySerializer


class PropertyListView(ListAPIView):
    """Property List View"""

    queryset = Property.objects.all()
    serializer_class = PropertySerializer

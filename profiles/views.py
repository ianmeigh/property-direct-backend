from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from .models import Profile
from .serializers import ProfileSerializer, ProfileSerializerAuthenticated


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        """Return different serializers based on authentication status

        Authenticated users are able to see profile contact information.
        """
        if self.request.user.is_authenticated:
            return ProfileSerializerAuthenticated
        else:
            return ProfileSerializer


class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        """Return different serializers based on authentication status.

        Authenticated users are able to see profile contact information.
        """
        if self.request.user.is_authenticated:
            return ProfileSerializerAuthenticated
        else:
            return ProfileSerializer

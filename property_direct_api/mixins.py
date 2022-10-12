class IsOwnerQuerysetFilter:
    def get_queryset(self):
        """Filter queryset to only objects where the currently authenticated
        user is the owner."""
        current_user = self.request.user
        if current_user.is_anonymous:
            queryset = self.model.objects.none()
        else:
            queryset = self.model.objects.filter(owner=current_user)
        return queryset

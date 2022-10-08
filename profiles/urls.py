from django.urls import path

from .views import ProfileDetailView, ProfileListView

urlpatterns = [
    path("profiles/", ProfileListView.as_view()),
    path("profiles/<int:pk>/", ProfileDetailView.as_view()),
]

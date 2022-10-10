from django.urls import path

from .views import FollowerDetailView, FollowerListView

urlpatterns = [
    path("followers/", FollowerListView.as_view()),
    path("followers/<int:pk>/", FollowerDetailView.as_view()),
]

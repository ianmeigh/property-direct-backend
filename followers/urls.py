from django.urls import path

from .views import FollowerListView

urlpatterns = [
    path("followers/", FollowerListView.as_view()),
]

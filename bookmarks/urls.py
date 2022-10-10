from django.urls import path

from .views import BookmarkListView

urlpatterns = [
    path("bookmarks/", BookmarkListView.as_view()),
]

from django.urls import path

from .views import BookmarkDetailView, BookmarkListView

urlpatterns = [
    path("bookmarks/", BookmarkListView.as_view()),
    path("bookmarks/<int:pk>/", BookmarkDetailView.as_view()),
]

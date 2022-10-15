from django.urls import path

from .views import NoteDetailView, NoteListView

urlpatterns = [
    path("notes/", NoteListView.as_view()),
    path("notes/<int:pk>/", NoteDetailView.as_view()),
]

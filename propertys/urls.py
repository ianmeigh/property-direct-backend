from django.urls import path

from .views import PropertyCreateView, PropertyDetailView, PropertyListView

urlpatterns = [
    path("property/", PropertyListView.as_view()),
    path("property/create", PropertyCreateView.as_view()),
    path("property/<int:pk>", PropertyDetailView.as_view()),
]

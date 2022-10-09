from django.urls import path

from .views import PropertyListView

urlpatterns = [
    path("property/", PropertyListView.as_view()),
]

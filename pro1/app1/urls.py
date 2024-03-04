from django.urls import path
from .views import BookView, details_api

urlpatterns = [
    path('add/', BookView),
    path('add/<int:pk>/', details_api)
]
from django.urls import path
from .views import *

urlpatterns = [
    path('author/', AuthorCreateView.as_view()),
    path('author/<int:pk>/', AuthorUpdateDelete.as_view()),
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view()),
]

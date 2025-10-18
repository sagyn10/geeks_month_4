# books/urls.py
from django.urls import path
from .views import (
    BooksListView,
    BooksDetailView,
    FirstTimeView,
    RandomNumbersView,
    ShowBiographyView,
)


urlpatterns = [
    path('', BooksListView.as_view(), name='books_list'),
    path('book_detail/<int:id>/', BooksDetailView.as_view(), name='books_detail'),
    path('time/', FirstTimeView.as_view(), name='first_time'),
    path('random_number/', RandomNumbersView.as_view(), name='random_number'),
    path('biography/', ShowBiographyView.as_view(), name='show_biography'),
]

# books/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('', views.book_list_view, name='books_list'),
    path('book_detail/<int:id>/', views.book_detail_view, name='books_detail'),
    path('time/', views.first_time_view, name='first_time'),
    path('random_number/', views.random_nambers_list, name='random_number'),
    path('biography/', views.show_biography, name='show_biography'),
]

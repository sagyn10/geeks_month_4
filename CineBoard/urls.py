from django.urls import path
from .views import (
    RegisterView,
    CustomLoginView,
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    CineRedirectView,
    SimpleRegisterView,
    SimpleLoginView,
)

app_name = 'CineBoard'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/add/', MovieCreateView.as_view(), name='movie_add'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/edit/', MovieUpdateView.as_view(), name='movie_edit'),
    path('movies/<int:pk>/delete/', MovieDeleteView.as_view(), name='movie_delete'),
    path('go/', CineRedirectView.as_view(), name='go'),
    path('simple-register/', SimpleRegisterView.as_view(), name='simple_register'),
    path('simple-login/', SimpleLoginView.as_view(), name='simple_login'),
]

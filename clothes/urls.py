from django.urls import path
from .views import (
    ItemListView,
    ItemDetailView,
    CategoryListView,
    MenListView,
    WomenListView,
    KidsListView,
    MenDetailView,
    WomenDetailView,
    KidsDetailView,
)

app_name = 'clothes'

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category_view'),
    path('men/', MenListView.as_view(), name='men'),
    path('women/', WomenListView.as_view(), name='women'),
    path('kids/', KidsListView.as_view(), name='kids'),
    path('men/<int:pk>/', MenDetailView.as_view(), name='men_detail'),
    path('women/<int:pk>/', WomenDetailView.as_view(), name='women_detail'),
    path('kids/<int:pk>/', KidsDetailView.as_view(), name='kids_detail'),
]

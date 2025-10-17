from django.urls import path
from . import views

app_name = 'clothes'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path('men/', views.men_list, name='men'),
    path('women/', views.women_list, name='women'),
    path('kids/', views.kids_list, name='kids'),
    path('men/<int:pk>/', views.men_detail, name='men_detail'),
    path('women/<int:pk>/', views.women_detail, name='women_detail'),
    path('kids/<int:pk>/', views.kids_detail, name='kids_detail'),
]

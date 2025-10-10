from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.order_add, name='order_add'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
]

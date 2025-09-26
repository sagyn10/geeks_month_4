from django.urls import path
from . import views



urlpatterns = [
    path('time/', views.first_time_view, name='first_time'),
    path('random_number/', views.random_nambers_list, name='random_number'),
    path('biography/', views.show_biography, name='show_biography')

]

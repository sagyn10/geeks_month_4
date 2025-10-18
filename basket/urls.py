from django.urls import path
from .views import (
    CustomerListView,
    AddCustomerView,
    CustomerDetailView,
    CustomerUpdateView,
    CustomerDeleteView,
    OrderListView,
)

app_name = 'basket'


urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('add/', AddCustomerView.as_view(), name='add_customer'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('<int:pk>/edit/', CustomerUpdateView.as_view(), name='edit_customer'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='delete_customer'),

    path('orders/', OrderListView.as_view(), name='order_list'),
]

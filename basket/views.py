from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Customer
from .models import Books


# 🔹 Список заказов
def order_list(request):
    customers = Customer.objects.all()
    return render(request, 'order_list.html', {'customers': customers})




# 🔹 Отображение списка покупателей
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})


# 🔹 Добавление нового покупателя
def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        book_id = request.POST.get('book')

        book = get_object_or_404(Books, id=book_id)

        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            book=book
        )

        return redirect('customer_list')

    books = Books.objects.all()
    return render(request, 'add_customer.html', {'books': books})


# 🔹 Детали конкретного покупателя
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_detail.html', {'customer': customer})

# 🔹 Удаление покупателя
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'delete_customer.html', {'customer': customer})


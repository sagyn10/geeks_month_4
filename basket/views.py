from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Customer
from .models import Books


# 🔹 Список заказов
def order_list(request):
    customers = Customer.objects.all()
    return render(request, 'basket/order_list.html', {'customers': customers})




# 🔹 Отображение списка покупателей
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'basket/customer_list.html', {'customers': customers})


# 🔹 Добавление нового покупателя
def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        book_id = request.POST.get('book') or request.GET.get('book')
        if not book_id:
            # если нет книги в запросе — перенаправим обратно на список
            return redirect('basket:customer_list')

        book = get_object_or_404(Books, id=book_id)
        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            book=book
        )

    return redirect('basket:customer_list')

    books = Books.objects.all()
    # если передан GET-параметр book — преобразуем в int для сравнения в шаблоне
    preselected = request.GET.get('book')
    try:
        preselected = int(preselected) if preselected else None
    except ValueError:
        preselected = None
    return render(request, 'basket/add_customer.html', {'books': books, 'preselected': preselected})


# 🔹 Детали конкретного покупателя
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'basket/customer_detail.html', {'customer': customer})

# 🔹 Удаление покупателя
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'basket/delete_customer.html', {'customer': customer})


def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        book_id = request.POST.get('book')
        if book_id:
            customer.book = get_object_or_404(Books, id=book_id)
        customer.save()
        return redirect('basket:customer_detail', pk=customer.pk)

    books = Books.objects.all()
    return render(request, 'basket/edit_customer.html', {'customer': customer, 'books': books})


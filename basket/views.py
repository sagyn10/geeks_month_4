from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Customer
from .forms import CustomerForm


# === Список заказов ===
def order_list(request):
    orders = Customer.objects.all().order_by('-id')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'basket/order_list.html', {
        'orders': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    })


# === Создание нового заказа ===
def order_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('basket:order_list')
    else:
        form = CustomerForm()
    return render(request, 'basket/order_form.html', context={'form': form})


# === Редактирование заказа ===
def order_edit(request, pk):
    order = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('basket:order_list')
    else:
        form = CustomerForm(instance=order)
    return render(request, 'basket/order_form.html', context= {'form': form})


# === Удаление заказа ===
def order_delete(request, pk):
    order = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('basket:order_list')
    return render(request, 'basket/order_confirm_delete.html', context={'order': order})
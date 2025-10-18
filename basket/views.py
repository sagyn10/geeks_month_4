from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Customer
from .models import Books


from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView

class OrderListView(ListView):
    model = Customer
    template_name = 'basket/order_list.html'
    context_object_name = 'customers'




class CustomerListView(ListView):
    model = Customer
    template_name = 'basket/customer_list.html'
    context_object_name = 'customers'





class AddCustomerView(View):
    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        preselected = request.GET.get('book')
        try:
            preselected = int(preselected) if preselected else None
        except ValueError:
            preselected = None
        return render(request, 'basket/add_customer.html', {'books': books, 'preselected': preselected})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        book_id = request.POST.get('book') or request.GET.get('book')
        if not book_id:
            return redirect('basket:customer_list')
        book = get_object_or_404(Books, id=book_id)
        Customer.objects.create(name=name, email=email, phone=phone, address=address, book=book)
        return redirect('basket:customer_list')


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'basket/customer_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'customer'


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'basket/delete_customer.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('basket:customer_list')



class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'basket/edit_customer.html'
    fields = ['name', 'email', 'phone', 'address', 'book']
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('basket:customer_detail', kwargs={'pk': self.object.pk})


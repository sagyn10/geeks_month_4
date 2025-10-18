# books/views.py (Class Based Views)
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from .models import Books, Reviews
from datetime import datetime
import random
from django.db.models import Avg


class BooksListView(ListView):
    model = Books
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BooksDetailView(DetailView):
    model = Books
    template_name = 'books/book_detail.html'
    pk_url_kwarg = 'id'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = book.reviews.order_by('-created_at').all()
        avg_rating = book.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        context.update({'reviews': reviews, 'avg_rating': round(avg_rating, 2)})
        return context

    def post(self, request, *args, **kwargs):
        # Поддерживаем добавление отзыва через форму на странице
        book = self.get_object()
        if 'review_submit' in request.POST:
            try:
                rating = int(request.POST.get('rating', 1))
            except ValueError:
                rating = 1
            text = request.POST.get('text', '').strip()
            if text:
                Reviews.objects.create(book=book, rating=rating, text=text)
        return redirect('books_detail', id=book.id)


class FirstTimeView(View):
    def get(self, request, *args, **kwargs):
        time_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return HttpResponse(time_str)


class RandomNumbersView(View):
    def get(self, request, *args, **kwargs):
        number = random.randint(1, 6)
        texts = {
            1: 'Выпало случайное число 1',
            2: 'Выпало случайное число 2',
            3: 'Выпало случайное число 3',
            4: 'Выпало случайное число 4',
            5: 'Выпало случайное число 5',
            6: 'Выпало случайное число 6',
        }
        return HttpResponse(texts[number])


class ShowBiographyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("""
            Привет, меня зовут Амантур. Кратко расскажу о себе, мне 17 лет.
            Я учусь в школе. Увлекаюсь боксом и баскетболом.
            На этом всё. Пока!!
        """)

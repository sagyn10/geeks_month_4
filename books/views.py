# books/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Books, Reviews
from datetime import datetime
import random
from django.db.models import Avg

def book_list_view(request):
    books = Books.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail_view(request, id):
    book = get_object_or_404(Books, id=id)
    reviews = book.reviews.order_by('-created_at').all()

    # Добавление отзыва (POST)
    if request.method == "POST" and 'review_submit' in request.POST:
        try:
            rating = int(request.POST.get('rating', 1))
        except ValueError:
            rating = 1
        text = request.POST.get('text', '').strip()
        if text:
            Reviews.objects.create(book=book, rating=rating, text=text)
            return redirect('books_detail', id=book.id)

    # Средняя оценка (если есть)
    avg_rating = book.reviews.aggregate(avg=Avg('rating'))['avg']
    if avg_rating is None:
        avg_rating = 0

    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 2),
    }
    return render(request, 'books/book_detail.html', context)

def first_time_view(request):
    time_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return HttpResponse(time_str)

def random_nambers_list(request):
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

def show_biography(request):
    return HttpResponse("""
        Привет, меня зовут Амантур. Кратко расскажу о себе, мне 17 лет.
        Я учусь в школе. Увлекаюсь боксом и баскетболом.
        На этом всё. Пока!!
    """)

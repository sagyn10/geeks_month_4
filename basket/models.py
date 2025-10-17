from django.db import models
from books.models import Books  # связь с таблицей книг

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name='Выбранная книга')

    def __str__(self):
        return f"{self.name} — {self.book.title}"

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        
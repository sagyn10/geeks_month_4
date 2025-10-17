# books/models.py
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Books(models.Model):
    images = models.ImageField(upload_to='books/', verbose_name='Обложка!')
    title = models.CharField(max_length=100, verbose_name='Название книги!')
    description = models.TextField(verbose_name='Описание книги!')
    quatity_page = models.PositiveIntegerField(default=1, verbose_name='Количество страниц')
    author = models.CharField(max_length=100, blank=True, verbose_name='Укажите автора!')
    book_audio = models.URLField(verbose_name='Укажите ссылку с ютуба!')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания книги!')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reviews(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        verbose_name='поставьте оценку от 1 до 5',
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    text = models.TextField(default='Прикольная книга', verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book} - {self.rating}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Person(models.Model):
    name = models.CharField(max_length=100, default="Нурсултан", verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Туриста"
        verbose_name_plural = "Туристы"


class Tour(models.Model):
    passport = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='driver')
    tour_at = models.CharField(max_length=100, default='Япония', verbose_name='Место тура')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tour_at} - {self.passport.name}'

    class Meta:
        verbose_name = 'тур'
        verbose_name_plural = 'туры'

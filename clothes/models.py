from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='clothes/', blank=True, null=True, verbose_name='Фото')
    categories = models.ManyToManyField(Category, related_name='items', blank=True, verbose_name='Категории')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

from django.db import models



class Books(models.Model):
    images = models.ImageField(upload_to='books/', verbose_name='Обложка!')
    title = models.CharField(max_length=100, verbose_name='Название книги!')
    description = models.TextField(verbose_name='Описание книги!')
    quatity_page = models.PositiveIntegerField(default=1, verbose_name='Количество страниц')
    author = models.CharField(max_length=100, blank=True, verbose_name='Укажите автора!' )
    book_audio = models.URLField(verbose_name='Укажите ссылку с ютуба!')
    created_at = models.CharField(verbose_name='Дата создания книги!')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Книгу'
        verbose_name_plural = 'Книги'
        
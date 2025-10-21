from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Genre(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=120, unique=True, blank=True)

	class Meta:
		verbose_name = 'Жанр'
		verbose_name_plural = 'Жанры'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		# Автоматически создаём slug из name, если он не указан
		if not self.slug and self.name:
			# преобразовать кириллицу в похожую латиницу простым транслитом через slugify
			# slugify не транслитерирует кириллицу в латиницу по умолчанию,
			# но он удалит недопустимые символы и приведёт к безопасному значению.
			# Для русских названий попробуем транслитеровать через простую замену
			# если slugify вернёт пустую строку.
			candidate = slugify(self.name)
			if not candidate:
				# fallback: заменить пробелы и не-латинские символы на '-' и ascii-символы
				candidate = ''.join(c if ord(c) < 128 else '-' for c in self.name)
				candidate = slugify(candidate)
			self.slug = candidate
		super().save(*args, **kwargs)


class Movie(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название')
	description = models.TextField(blank=True, verbose_name='Описание')
	year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Год')
	genres = models.ManyToManyField(Genre, related_name='movies', blank=True, verbose_name='Жанры')
	image = models.ImageField(upload_to='cine_images/', null=True, blank=True, verbose_name='Обложка')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

	def __str__(self):
		return f"{self.title} ({self.year})" if self.year else self.title

	class Meta:
		verbose_name = 'Фильм'
		verbose_name_plural = 'Фильмы'


class Rating(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
	user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
	rating = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Оценка'
		verbose_name_plural = 'Оценки'

	def __str__(self):
		return f"{self.movie.title}: {self.rating}"

from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'year', 'created_at')
	search_fields = ('title',)

from .models import Genre, Rating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	exclude = ('slug',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ('movie', 'rating', 'user', 'created_at')
	list_filter = ('rating',)

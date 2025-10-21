from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from .models import Movie, Genre, Rating
from django.db.models import Avg
from .forms import SimpleRegisterForm, SimpleLoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


class RegisterView(FormView):
	template_name = 'CineBoard/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('accounts:login')

	def form_valid(self, form):
		user = form.save()
		return super().form_valid(form)


class CustomLoginView(LoginView):
	template_name = 'CineBoard/login.html'
	authentication_form = AuthenticationForm


class MovieListView(ListView):
	model = Movie
	template_name = 'CineBoard/movie_list.html'
	context_object_name = 'movies'

	def get_queryset(self):
		qs = super().get_queryset().all()
		# аннотируем средний рейтинг для каждого фильма
		qs = qs.annotate(avg_rating=Avg('ratings__rating'))
		# фильтр по жанру (query param: genre=slug)
		genre_slug = self.request.GET.get('genre')
		if genre_slug:
			qs = qs.filter(genres__slug=genre_slug)
		# поиск по title
		q = self.request.GET.get('q', '').strip()
		if q:
			qs = qs.filter(title__icontains=q)
		# сортировка: ?sort=rating -> by average rating desc
		sort = self.request.GET.get('sort')
		if sort == 'rating':
			qs = qs.order_by('-avg_rating')
		else:
			qs = qs.order_by('-created_at')
		return qs

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['genres'] = Genre.objects.all()
		ctx['current_genre'] = self.request.GET.get('genre')
		ctx['sort'] = self.request.GET.get('sort')
		return ctx


class MovieDetailView(DetailView):
	model = Movie
	template_name = 'CineBoard/movie_detail.html'
	context_object_name = 'movie'
	pk_url_kwarg = 'pk'

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		movie = self.get_object()
		avg = movie.ratings.aggregate(avg=Avg('rating'))['avg'] or 0
		ctx.update({'avg_rating': round(avg, 2), 'ratings': movie.ratings.all()})
		return ctx

	def post(self, request, *args, **kwargs):
		# только авторизованные пользователи могут оставлять оценки
		if not request.user.is_authenticated:
			# перенаправим на общий путь входа accounts:login с параметром next
			login_url = reverse('accounts:login')
			return redirect(f"{login_url}?next={request.path}")

		# добавить оценку (поле rating в POST)
		movie = self.get_object()
		try:
			value = int(request.POST.get('rating'))
		except (TypeError, ValueError):
			value = None
		if value and 1 <= value <= 10:
			Rating.objects.create(movie=movie, user=request.user, rating=value, comment=request.POST.get('comment', ''))
		return redirect('CineBoard:movie_detail', pk=movie.pk)


class MovieCreateView(LoginRequiredMixin, CreateView):
	model = Movie
	fields = ['title', 'description', 'year', 'genres', 'image']
	template_name = 'CineBoard/movie_form.html'
	success_url = reverse_lazy('CineBoard:movie_list')


class MovieUpdateView(LoginRequiredMixin, UpdateView):
	model = Movie
	fields = ['title', 'description', 'year', 'genres', 'image']
	template_name = 'CineBoard/movie_form.html'
	pk_url_kwarg = 'pk'

	def get_success_url(self):
		return reverse_lazy('CineBoard:movie_detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(LoginRequiredMixin, DeleteView):
	model = Movie
	template_name = 'CineBoard/movie_confirm_delete.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('CineBoard:movie_list')



class CineRedirectView(View):
	"""Redirect helper: anonymous -> registration, authenticated -> movies list"""
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('CineBoard:movie_list'))
		return HttpResponseRedirect(reverse('accounts:register'))


class SimpleRegisterView(FormView):
	template_name = 'CineBoard/simple_register.html'
	form_class = SimpleRegisterForm
	success_url = reverse_lazy('accounts:login')

	def form_valid(self, form):
		user = form.save()
		messages.success(self.request, 'Регистрация прошла успешно. Пожалуйста, войдите в аккаунт.')
		return super().form_valid(form)


class SimpleLoginView(FormView):
	template_name = 'CineBoard/simple_login.html'
	form_class = SimpleLoginForm
	success_url = reverse_lazy('CineBoard:movie_list')

	def form_valid(self, form):
		first = form.cleaned_data['first_name']
		last = form.cleaned_data['last_name']
		password = form.cleaned_data['password']
		user = authenticate(self.request, username__iexact=None, password=password)
		# authenticate по имени/фамилии: найдём пользователя
		from django.contrib.auth import get_user_model
		User = get_user_model()
		try:
			user_obj = User.objects.filter(first_name__iexact=first, last_name__iexact=last).first()
		except Exception:
			user_obj = None
		if user_obj:
			user = authenticate(self.request, username=user_obj.username, password=password)
		if user is not None:
			login(self.request, user)
			return super().form_valid(form)
		form.add_error(None, 'Неверные данные для входа')
		return self.form_invalid(form)


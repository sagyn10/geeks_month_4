from django.shortcuts import render, get_object_or_404
from django.db.utils import OperationalError, ProgrammingError
from django.views.generic import ListView, DetailView
from .models import Item, Category


class DbErrorMixin:
    """Миксин для перехвата ошибок БД и возврата понятного шаблона"""
    def handle_db_error(self, e):
        return render(self.request, 'clothes/db_migration_required.html', {'error': str(e)})


class ItemListView(ListView, DbErrorMixin):
    model = Item
    template_name = 'clothes/item_list.html'
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        try:
            qs = self.model.objects.all()
            if q:
                qs = qs.filter(title__icontains=q)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)
        self.object_list = qs
        context = self.get_context_data(object_list=qs, q=q, current_section='all')
        return self.render_to_response(context)


class ItemDetailView(DetailView, DbErrorMixin):
    model = Item
    template_name = 'clothes/item_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)


class CategoryListView(ListView, DbErrorMixin):
    model = Item
    template_name = 'clothes/item_list.html'
    context_object_name = 'items'

    def get(self, request, slug=None, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        try:
            category = get_object_or_404(Category, slug=slug)
            qs = category.items.all()
            if q:
                qs = qs.filter(title__icontains=q)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)
        section = slug if slug in ('men', 'women', 'kids') else 'all'
        self.object_list = qs
        context = self.get_context_data(object_list=qs, category=category, current_section=section)
        return self.render_to_response(context)


class MenListView(ListView, DbErrorMixin):
    model = Item
    template_name = 'clothes/men_list.html'
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        try:
            category = get_object_or_404(Category, slug='men')
            qs = category.items.all().order_by('price')
            if q:
                qs = qs.filter(title__icontains=q)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)
        self.object_list = qs
        context = self.get_context_data(object_list=qs, category=category, q=q, current_section='men')
        return self.render_to_response(context)


class WomenListView(ListView, DbErrorMixin):
    model = Item
    template_name = 'clothes/women_list.html'
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        try:
            category = get_object_or_404(Category, slug='women')
            qs = category.items.all().order_by('-created_at')
            if q:
                qs = qs.filter(title__icontains=q)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)
        self.object_list = qs
        context = self.get_context_data(object_list=qs, category=category, q=q, current_section='women')
        return self.render_to_response(context)


class KidsListView(ListView, DbErrorMixin):
    model = Item
    template_name = 'clothes/kids_list.html'
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        try:
            category = get_object_or_404(Category, slug='kids')
            qs = category.items.all().filter(price__lte=1000)
            if q:
                qs = qs.filter(title__icontains=q)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)
        self.object_list = qs
        context = self.get_context_data(object_list=qs, category=category, q=q, current_section='kids')
        return self.render_to_response(context)


class MenDetailView(DetailView, DbErrorMixin):
    model = Item
    template_name = 'clothes/men_detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        category = get_object_or_404(Category, slug='men')
        return get_object_or_404(Item, pk=self.kwargs.get('pk'), categories=category)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)


class WomenDetailView(DetailView, DbErrorMixin):
    model = Item
    template_name = 'clothes/women_detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        category = get_object_or_404(Category, slug='women')
        return get_object_or_404(Item, pk=self.kwargs.get('pk'), categories=category)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)


class KidsDetailView(DetailView, DbErrorMixin):
    model = Item
    template_name = 'clothes/kids_detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        category = get_object_or_404(Category, slug='kids')
        return get_object_or_404(Item, pk=self.kwargs.get('pk'), categories=category)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except (OperationalError, ProgrammingError) as e:
            return self.handle_db_error(e)


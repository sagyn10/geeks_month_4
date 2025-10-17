from django.shortcuts import render, get_object_or_404
from django.db.utils import OperationalError, ProgrammingError
from .models import Item
from .models import Category


def item_list(request):
    q = request.GET.get('q', '').strip()
    try:
        items = Item.objects.all()
        if q:
            items = items.filter(title__icontains=q)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/item_list.html', {'items': items, 'q': q, 'current_section': 'all'})


def item_detail(request, pk):
    try:
        item = get_object_or_404(Item, pk=pk)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/item_detail.html', {'item': item})


def category_view(request, slug):
    q = request.GET.get('q', '').strip()
    try:
        category = get_object_or_404(Category, slug=slug)
        items = category.items.all()
        if q:
            items = items.filter(title__icontains=q)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    # определить секцию для подсветки кнопки
    section = slug if slug in ('men', 'women', 'kids') else 'all'
    return render(request, 'clothes/item_list.html', {'items': items, 'category': category, 'current_section': section})


def men_list(request):
    # логика для мужской одежды: сортировка по цене возрастанию
    q = request.GET.get('q', '').strip()
    try:
        category = get_object_or_404(Category, slug='men')
        items = category.items.all().order_by('price')
        if q:
            items = items.filter(title__icontains=q)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/men_list.html', {'items': items, 'category': category, 'q': q, 'current_section': 'men'})


def women_list(request):
    # логика для женской одежды: последние добавленные в начале
    q = request.GET.get('q', '').strip()
    try:
        category = get_object_or_404(Category, slug='women')
        items = category.items.all().order_by('-created_at')
        if q:
            items = items.filter(title__icontains=q)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/women_list.html', {'items': items, 'category': category, 'q': q, 'current_section': 'women'})


def kids_list(request):
    # логика для детской одежды: фильтр по цене <= 1000 (демо)
    q = request.GET.get('q', '').strip()
    try:
        category = get_object_or_404(Category, slug='kids')
        items = category.items.all().filter(price__lte=1000)
        if q:
            items = items.filter(title__icontains=q)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/kids_list.html', {'items': items, 'category': category, 'q': q, 'current_section': 'kids'})


def men_detail(request, pk):
    try:
        category = get_object_or_404(Category, slug='men')
        item = get_object_or_404(Item, pk=pk, categories=category)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/men_detail.html', {'item': item, 'category': category})


def women_detail(request, pk):
    try:
        category = get_object_or_404(Category, slug='women')
        item = get_object_or_404(Item, pk=pk, categories=category)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/women_detail.html', {'item': item, 'category': category})


def kids_detail(request, pk):
    try:
        category = get_object_or_404(Category, slug='kids')
        item = get_object_or_404(Item, pk=pk, categories=category)
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'clothes/db_migration_required.html', {'error': str(e)})
    return render(request, 'clothes/kids_detail.html', {'item': item, 'category': category})

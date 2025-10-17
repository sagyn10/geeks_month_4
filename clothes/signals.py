from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    # только для приложения clothes
    if sender.name != 'clothes':
        return
    Category = apps.get_model('clothes', 'Category')
    defaults = [
        ('одежда мужская', 'men'),
        ('одежда женская', 'women'),
        ('детская одежда', 'kids'),
    ]
    for name, slug in defaults:
        Category.objects.get_or_create(slug=slug, defaults={'name': name})

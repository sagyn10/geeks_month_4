from django.contrib import admin
from .models import Item, Category


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'preview')
    search_fields = ('title',)
    list_filter = ('categories',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' style='max-height:60px;'/>"
        return '-'
    preview.allow_tags = True
    preview.short_description = 'Превью'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

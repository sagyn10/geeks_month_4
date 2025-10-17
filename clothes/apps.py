from django.apps import AppConfig


class ClothesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clothes'

    def ready(self):
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass

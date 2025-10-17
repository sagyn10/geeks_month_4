from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        try:
            from . import signals  # noqa: F401
        except Exception:
            # при запуске в среде анализа импорт может не разрешиться — безопасно игнорируем
            pass

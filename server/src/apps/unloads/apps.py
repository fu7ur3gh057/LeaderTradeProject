from django.apps import AppConfig


class UnloadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.unloads"
    verbose_name = "Выгрузки"

    def ready(self) -> None:
        import src.apps.unloads.signals

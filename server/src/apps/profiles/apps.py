from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.profiles"
    verbose_name = "Профили"

    def ready(self) -> None:
        import src.apps.profiles.signals

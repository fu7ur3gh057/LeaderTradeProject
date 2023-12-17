from django.core.management.base import BaseCommand

from src.apps.base.models import Settings


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        # The magic line
        if Settings.objects.count() == 0:
            Settings.objects.create()
            print("Settings created")

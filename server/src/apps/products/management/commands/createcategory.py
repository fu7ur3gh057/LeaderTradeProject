from django.core.management import BaseCommand

from src.apps.products.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        # The magic line
        if Category.objects.count() == 0:
            Category.objects.create(title="Шины")
            Category.objects.create(title="Диски")
            Category.objects.create(title="Аксессуары")
            print("Categories created")

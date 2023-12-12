from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.orders.models import Basket, Favorites
from src.apps.profiles.models import Profile


@receiver(post_save, sender=Profile)
def create_basket_signal(sender, instance: Profile, created: bool, **kwargs) -> None:
    if created:
        Basket.objects.create(profile=instance)


@receiver(post_save, sender=Profile)
def create_favorites_signal(sender, instance: Profile, created: bool, **kwargs) -> None:
    if created:
        Favorites.objects.create(profile=instance)

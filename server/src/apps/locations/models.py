from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField

from src.apps.base.models import PKIDMixin, TimeStampedMixin
from src.other.enums import DayOfWeek


class City(PKIDMixin, TimeStampedMixin):
    title = models.CharField(max_length=100, verbose_name=_("Название"))

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")

    def __str__(self) -> str:
        return self.title


class Address(PKIDMixin, TimeStampedMixin):
    city = models.ForeignKey(
        to=City,
        related_name="addresses",
        on_delete=models.CASCADE,
        verbose_name=_("Город"),
    )
    street = models.CharField(max_length=100, verbose_name=_("Улица"))
    house = models.CharField(max_length=100, verbose_name=_("Дом"))
    apartment = models.CharField(max_length=100, verbose_name=_("Квартира"))

    class Meta:
        verbose_name = _("Адрес")
        verbose_name_plural = _("Адресы")

    def __str__(self) -> str:
        return self.street


class Shop(PKIDMixin, TimeStampedMixin):
    address = models.ForeignKey(
        to=Address,
        related_name="shops",
        on_delete=models.CASCADE,
        verbose_name=_("Адрес"),
    )
    email = models.CharField(max_length=255, verbose_name=_("Почта"))
    latitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
        verbose_name=_("Широта"),
    )
    longitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        null=True,
        blank=True,
        verbose_name=_("Долгота"),
    )

    class Meta:
        verbose_name = _("Магазин")
        verbose_name_plural = _("Магазины")

    def __str__(self) -> str:
        return self.email


class Worktime(PKIDMixin):
    shop = models.ForeignKey(
        to=Shop,
        related_name="work_times",
        on_delete=models.CASCADE,
        verbose_name=_("Магазин"),
    )
    day_of_week = EnumChoiceField(
        DayOfWeek, default=DayOfWeek.MONDAY, verbose_name=_("День недели")
    )
    start_time = models.TimeField(verbose_name=_("Время начала работы"))
    end_time = models.TimeField(verbose_name=_("Время завершения работы"))

    class Meta:
        verbose_name = _("Время Работы")
        verbose_name_plural = _("Время Работы")

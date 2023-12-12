from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.base.models import PKIDMixin, TimeStampedMixin


class PromoCode(PKIDMixin, TimeStampedMixin):
    products = models.ManyToManyField(
        to="products.Product",
        related_name="promocodes",
        blank=True,
        verbose_name=_("Товары"),
    )
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    code = models.CharField(max_length=50, verbose_name=_("КОД"))
    percent_discount = models.IntegerField(verbose_name=_("Скидка в процентах"))
    amount_discount = models.DecimalField(
        max_digits=8, decimal_places=3, verbose_name=_("Фиксированная сумма скидки")
    )
    all_products = models.BooleanField(
        default=False,
        verbose_name=_("Все продукты"),
        help_text=_("Действует на все продукты"),
    )
    expire_time = models.DateTimeField(verbose_name=_("Дата завершения"))
    is_active = models.BooleanField(verbose_name=_("Активно"))

    class Meta:
        verbose_name = _("Промокод")
        verbose_name_plural = _("Промокоды")

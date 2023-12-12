from django.db import models
from django.utils.translation import gettext_lazy as _
from src.apps.base.models import TimeStampedMixin, PKIDMixin


class Banner(PKIDMixin, TimeStampedMixin):
    image = models.ImageField(verbose_name=_("Изображение"))
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")

    def __str__(self) -> str:
        return self.title

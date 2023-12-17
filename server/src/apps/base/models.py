from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class PKIDMixin(models.Model):
    pk_id = models.BigAutoField(primary_key=True, editable=False, verbose_name=_("ID"))

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Время создания")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Последнее обновление")
    )

    class Meta:
        abstract = True


class Settings(models.Model):
    verify_token_max_count = models.IntegerField(
        default=1,
        verbose_name=_("Количество СМС"),
        help_text=_("Попыток верификации за токен"),
    )
    verify_token_generation_period = models.IntegerField(
        default=5, verbose_name=_("Период геренации токена"), help_text="В минутах"
    )

    class Meta:
        verbose_name = _("Настройка")
        verbose_name_plural = _("Настройки")

    def save(self, *args, **kwargs) -> None:
        if self.pk is None:
            if len(Settings.objects.all()) > 0:
                raise NameError("Settings already exists")
        super(Settings, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return "Настройки"

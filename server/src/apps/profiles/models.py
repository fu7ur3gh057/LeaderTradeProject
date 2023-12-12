from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.base.models import PKIDMixin, TimeStampedMixin


class Profile(PKIDMixin, TimeStampedMixin):
    user = models.OneToOneField(
        to="users.User",
        related_name="profile",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
    )
    email = models.CharField(
        max_length=50, unique=True, blank=True, verbose_name=_("Почта")
    )
    full_name = models.CharField(max_length=250, blank=True, verbose_name=_("ФИО"))
    is_legal = models.BooleanField(default=False, verbose_name=_("Юридическое лицо"))
    city = models.ForeignKey(
        to="locations.City",
        related_name="profiles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Профиль")
        verbose_name_plural = _("Профиль")

    def __str__(self) -> str:
        return self.full_name


class LegalCard(PKIDMixin, TimeStampedMixin):
    profile = models.OneToOneField(
        to=Profile,
        related_name="card",
        on_delete=models.CASCADE,
        verbose_name=_("Профиль"),
    )
    title = models.CharField(
        max_length=512, blank=True, verbose_name=_("Наименование полное")
    )
    legal_address = models.CharField(
        max_length=215, blank=True, verbose_name=_("Юридический адрес")
    )
    email = models.CharField(
        max_length=215, blank=True, verbose_name=_("Почтовый адрес")
    )
    inn = models.IntegerField(blank=True, null=True, verbose_name=_("ИНН"))
    kpp = models.IntegerField(blank=True, null=True, verbose_name=_("КПП"))
    bik = models.IntegerField(blank=True, null=True, verbose_name=_("БИК"))
    ogrn = models.IntegerField(blank=True, null=True, verbose_name=_("ОГРН"))
    settlement = models.IntegerField(
        blank=True, null=True, verbose_name=_("Расчетный счет")
    )
    korr = models.IntegerField(blank=True, null=True, verbose_name=_("Корр счет"))
    general_director = models.CharField(
        max_length=100, blank=True, verbose_name=_("Генеральный директор")
    )

    class Meta:
        verbose_name = _("ЮР Карточка")
        verbose_name_plural = _("ЮР Карточки")

    def __str__(self) -> str:
        return f"{self.email} card"

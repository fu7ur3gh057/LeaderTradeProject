from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from src.apps.base.models import TimeStampedMixin, PKIDMixin
from src.apps.users.managers import UserManager
from src.utils.sms_utils import generate_verification_code


class User(AbstractBaseUser, PermissionsMixin, TimeStampedMixin):
    id = models.BigAutoField(primary_key=True, editable=False, verbose_name=_("ID"))
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name=_("Номер телефона"),
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self) -> str:
        return f"{self.phone_number}"


class Verification(PKIDMixin, TimeStampedMixin):
    user = models.OneToOneField(
        verbose_name=_("Пользователь"),
        to=User,
        related_name="verification",
        on_delete=models.CASCADE,
    )
    sms_code = models.IntegerField(verbose_name=_("Код"), null=True, blank=True)

    class Meta:
        verbose_name = _("Верификация")
        verbose_name_plural = _("Верификации")

    def is_fresh(self) -> bool:
        created = self.created_at
        return True

    def generate_code(self) -> int:
        if self.is_fresh():
            return generate_verification_code()
        return self.sms_code

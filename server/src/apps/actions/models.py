from django.core.validators import RegexValidator
from django.db import models
from django_enum_choices.fields import EnumChoiceField
from django.utils.translation import gettext_lazy as _

from src.apps.base.models import PKIDMixin, TimeStampedMixin
from src.other.enums import CallRequestStatus, FormApplicationStatus
from src.other.validators import phone_regex
from src.utils.slug_utils import slugify


class Portfolio(PKIDMixin, TimeStampedMixin):
    make = models.ForeignKey(
        to="catalog.Make",
        related_name="portfolios",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Марка"),
    )
    slug = models.SlugField(
        max_length=250, null=True, blank=True, unique=True, verbose_name=_("URL путь")
    )
    image = models.ImageField(
        upload_to="portfolios/",
        blank=True,
        null=True,
        verbose_name=_("Основное Изображение"),
    )
    description = models.TextField()
    product = models.ForeignKey(
        to="products.Product",
        related_name="portfolios",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Товар"),
    )

    def save(self, *args, **kwargs) -> None:
        if self.pk_id is None:
            self.image.upload_to = f"portfolios/{self.pk_id}/"
        self.slug = f"{slugify(self.make.title)}-{self.pk_id}"
        super(Portfolio, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Портфолио")
        verbose_name_plural = _("Портфолио")

    def __str__(self) -> str:
        return f"Портфолио {self.make.title}"


class PortfolioImage(PKIDMixin):
    portfolio = models.ForeignKey(
        to=Portfolio,
        related_name="gallery",
        on_delete=models.CASCADE,
        verbose_name=_("Портфолио"),
    )
    image = models.ImageField(
        upload_to="portfolios/", blank=True, null=True, verbose_name=_("Изображение")
    )

    class Meta:
        verbose_name = _("Изображение Портфолио")
        verbose_name_plural = _("Изображения Портфолио")

    def __str__(self) -> str:
        return f"Изображение {self.portfolio}"

    def save(self, *args, **kwargs) -> None:
        self.image.upload_to = f"portfolios/{self.portfolio.pk_id}/"
        super(PortfolioImage, self).save(*args, **kwargs)


class Review(PKIDMixin):
    client_name = models.CharField(max_length=255, verbose_name=_("Имя клиента"))
    image = models.ImageField(
        upload_to="reviews/", blank=True, null=True, verbose_name=_("Изображение")
    )
    text = models.TextField(verbose_name=_("Текст"))
    date = models.DateTimeField(verbose_name=_("Дата"))

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self) -> str:
        return f"Отзыв {self.pk_id}"

    def save(self, *args, **kwargs) -> None:
        self.image.upload_to = f"reviews/{self.pk_id}/"
        super(Review, self).save(*args, **kwargs)


class FormApplication(PKIDMixin, TimeStampedMixin):
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name=_("Номер телефона"),
    )
    status = EnumChoiceField(
        FormApplicationStatus,
        default=FormApplicationStatus.NEW,
        verbose_name=_("Статус"),
    )

    class Meta:
        verbose_name = _("Форма Заявки")
        verbose_name_plural = _("Формы Заявки")


class CallRequest(PKIDMixin, TimeStampedMixin):
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name=_("Номер телефона"),
    )
    status = EnumChoiceField(
        CallRequestStatus,
        default=CallRequestStatus.PRODUCT,
        verbose_name=_("Статус"),
    )

    class Meta:
        verbose_name = _("Запрос Звонка")
        verbose_name_plural = _("Запросы Звонков")

from datetime import date
from django.db import models
from froala_editor.fields import FroalaField
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit
from src.utils.slug_utils import slug_path


class Promo(models.Model):
    title = models.CharField("Заголовок", max_length=250)
    title2 = models.CharField("Заголовок 2", max_length=250, null=True, blank=True)
    desc = models.TextField("Описание", max_length=250, null=True, blank=True)
    button_link = models.CharField(
        "Ссылка на кнопке", max_length=300, null=True, blank=True
    )
    button_title = models.CharField(
        "Текст на кнопке", max_length=300, null=True, blank=True
    )
    def get_pic_path(self, filename):
        return slug_path("promo/%Y/%m", filename)

    pic = ProcessedImageField(
        verbose_name="фото",
        upload_to=get_pic_path,
        null=True,
        blank=True,
        processors=[ResizeToFit(860, 540, upscale=False)],
        options={"quality": 70},
    )

    start = models.DateField("Старт акции", default=date.today)
    end = models.DateField("Завершение акции", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"


class Portfolio(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=150)
    def get_pic_path(self, filename):
        return slug_path("portfolio/%Y/%m", filename)

    pic = ProcessedImageField(
        verbose_name="фото",
        upload_to=get_pic_path,
        null=True,
        blank=True,
        processors=[
            ResizeToFit(1000, 1000, upscale=False),
        ],
        options={"quality": 70},
    )
    content = FroalaField("Описание", blank=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'


class PortfolioImage(models.Model):
    def get_pic_path(self, filename):
        return slug_path("portfolio/%Y/%m", filename)

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='pics')

    pic = ProcessedImageField(
        verbose_name="фото",
        upload_to=get_pic_path,
        null=True,
        blank=True,
        processors=[
            ResizeToFit(1000, 1000, upscale=False),
        ],
        options={"quality": 70},
    )
    sort = models.IntegerField("порядок", default=0)

    class Meta:
        ordering = ("sort",)
        verbose_name = "Фото"
        verbose_name_plural = "Фото"


class PortfolioProduct(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, verbose_name="товар", related_name="+"
    )
    sort = models.IntegerField("порядок", default=0)

    class Meta:
        ordering = ("pk",)
        verbose_name = "Товар"
        verbose_name_plural = "Товары в Портфолио"
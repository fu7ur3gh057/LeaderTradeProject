from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from django.utils.translation import gettext_lazy as _

from src.apps.base.models import TimeStampedMixin, PKIDMixin
from src.utils.slug_utils import slugify


class Post(PKIDMixin, TimeStampedMixin, Page):
    # title = models.CharField(max_length=255, verbose_name=_("Название"))
    # slug = models.SlugField(
    #     max_length=250, null=True, blank=True, unique=True, verbose_name=_("URL путь")
    # )
    products = models.ManyToManyField(
        to="products.Product", related_name="news", verbose_name=_("Товары")
    )
    pic = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Обложка"),
        related_name="+",
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title", label="Заголовок")),
            ("paragraph", blocks.RichTextBlock(label="Текст")),
            ("image", ImageChooserBlock(label="Изображение")),
            (
                "gallery",
                blocks.ListBlock(ImageChooserBlock(label="Фото"), label="Галерея фото"),
            ),
        ],
        use_json_field=True,
        verbose_name=_("Контент"),
    )
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("pic"),
        FieldPanel("body"),
    ]
    date = models.DateTimeField("Дата новости")

    class Meta:
        verbose_name = _("Публикация")
        verbose_name_plural = _("Публикации")

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.id)

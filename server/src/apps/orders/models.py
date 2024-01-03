from typing import Any

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django_enum_choices.fields import EnumChoiceField

from src.apps.base.models import PKIDMixin, TimeStampedMixin
from products.models import Product
from src.other.enums import OrderStatus, DocumentType


# class OrderedProduct(PKIDMixin, TimeStampedMixin):
#     product = models.ForeignKey(to="products.Product", related_name="ordered_products", on_delete=models.CASCADE,)


class Order(PKIDMixin, TimeStampedMixin):
    profile = models.OneToOneField(
        to="profiles.Profile",
        related_name="orders",
        on_delete=models.CASCADE,
        verbose_name=_("Профиль"),
    )
    promo_code = models.ForeignKey(
        to="billing.PromoCode",
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Промокод"),
    )
    address = models.ForeignKey(
        to="locations.Address",
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Адрес"),
    )
    # products = models.ManyToManyField(
    #     to="products.Product", related_name="orders", verbose_name=_("Товары")
    # )
    # product_id: str, count: int, current_price: float
    products = models.JSONField(verbose_name=_("Товары"), null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=_("Имя"))
    surname = models.CharField(max_length=100, verbose_name=_("Фамилия"))
    patronymic = models.CharField(max_length=100, verbose_name=_("Отчество"))
    email = models.CharField(max_length=255, verbose_name=_("Электронная почта"))
    amount = models.DecimalField(
        max_digits=5, decimal_places=5, verbose_name=_("Сумма")
    )
    delivery = models.BooleanField(default=False, verbose_name=_("Доставка"))
    status = EnumChoiceField(
        OrderStatus, default=OrderStatus.NEW, verbose_name=_("Статус")
    )
    accepted = models.BooleanField(default=False, verbose_name=_("Подтвержден"))
    accept_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Время подтверждения")
    )

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def accept_order(self) -> None:
        self.accepted = True
        self.accept_date = timezone.localtime(timezone.now())
        self.save()

    @property
    def products_count(self) -> int:
        products: dict | None = self.products
        if products is None:
            return 0
        return len(products)

    @property
    def total_product_count(self) -> int:
        products: dict | None = self.products
        if products is None:
            return 0
        total_count = 0
        for product_id, product in products.items():
            total_count += product["count"]
        return total_count

    @property
    def total_price(self) -> float:
        products: dict | None = self.products
        if products is None:
            return 0
        total_price_list: float = 0
        for product_id, product in products.items():
            product_price: float = product["count"] * product["current_price"]
            total_price_list += product_price
        return total_price_list

    def __str__(self) -> str:
        return f"Заказ {self.profile}"


class Document(PKIDMixin, TimeStampedMixin):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    order = models.ForeignKey(
        to=Order,
        related_name="documents",
        on_delete=models.CASCADE,
        verbose_name=_("Заказ"),
    )
    type = EnumChoiceField(
        DocumentType, default=DocumentType.INVOICE, verbose_name=_("Тип")
    )
    file = models.FileField(upload_to="documents/", verbose_name=_("Файл"))

    def save(self, *args, **kwargs) -> None:
        self.file.upload_to = f"documents/{self.order.pk_id}/"
        super(Document, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Документ Заказа")
        verbose_name_plural = _("Документы Заказов")

    def __str__(self) -> str:
        return f"{self.title}"


class Basket(PKIDMixin, TimeStampedMixin):
    profile = models.OneToOneField(
        to="profiles.Profile",
        related_name="basket",
        on_delete=models.CASCADE,
        verbose_name=_("Профиль"),
    )
    # {product_id: count,} -> {"1":2}
    products = models.JSONField(blank=True, null=True, verbose_name=_("Товар корзины"))

    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")

    def get_products_count(self) -> int:
        total_count = 0
        for product_id, count in self.products.items():
            total_count += count
        return total_count

    def increase_product(self, product_id: str) -> None:
        if product_id in self.products:
            self.products[product_id] += 1
        else:
            self.products[product_id] = 1
        self.save()

    def decrease_product(self, product_id: str) -> None:
        if product_id not in self.products:
            return None
        count = self.products[product_id]
        if count <= 1:
            self.products.pop(product_id)
        else:
            count -= 1
            self.products[product_id] = count
        self.save()

    def __str__(self) -> str:
        return f"Корзина {self.profile}"


class Favorites(PKIDMixin, TimeStampedMixin):
    profile = models.OneToOneField(
        to="profiles.Profile",
        related_name="favorites",
        on_delete=models.CASCADE,
        verbose_name=_("Профиль"),
    )
    products = models.ManyToManyField(
        to="products.Product", related_name="favorites", verbose_name=_("Товары")
    )

    class Meta:
        verbose_name = _("Избранное")
        verbose_name_plural = _("Избранные")

    def add_product(self, product_id: int) -> QuerySet[Product]:
        product = Product.objects.filter(pk_id=product_id).first()
        if product not in self.products.all():
            self.products.add(product)
            self.save()
        return self.products.all()

    def remove_product(self, product_id: int) -> QuerySet[Product]:
        product = Product.objects.filter(pk_id=product_id).first()
        if product in self.products.all():
            self.products.remove(product)
            self.save()
        return self.products.all()

    def __str__(self) -> str:
        return f"Избранные {self.profile}"

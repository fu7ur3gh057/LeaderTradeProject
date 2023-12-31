# Generated by Django 4.2.6 on 2023-12-17 12:04

from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import src.other.enums


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("profiles", "0002_initial"),
        ("billing", "0001_initial"),
        ("products", "0001_initial"),
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "pk_id",
                    models.BigAutoField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Последнее обновление"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("surname", models.CharField(max_length=100, verbose_name="Фамилия")),
                (
                    "patronymic",
                    models.CharField(max_length=100, verbose_name="Отчество"),
                ),
                (
                    "email",
                    models.CharField(max_length=255, verbose_name="Электронная почта"),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=5, max_digits=5, verbose_name="Сумма"
                    ),
                ),
                (
                    "delivery",
                    models.BooleanField(default=False, verbose_name="Доставка"),
                ),
                (
                    "status",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[
                            ("new", "new"),
                            ("paid", "paid"),
                            ("awaiting", "awaiting"),
                            ("canceled", "canceled"),
                            ("accepted", "accepted"),
                        ],
                        default=src.other.enums.OrderStatus["NEW"],
                        enum_class=src.other.enums.OrderStatus,
                        max_length=8,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="locations.address",
                        verbose_name="Адрес",
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        related_name="orders",
                        to="products.product",
                        verbose_name="Товары",
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="profiles.profile",
                        verbose_name="Профиль",
                    ),
                ),
                (
                    "promo_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="billing.promocode",
                        verbose_name="Промокод",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
            },
        ),
        migrations.CreateModel(
            name="Favorites",
            fields=[
                (
                    "pk_id",
                    models.BigAutoField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Последнее обновление"
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        related_name="favorites",
                        to="products.product",
                        verbose_name="Товары",
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorites",
                        to="profiles.profile",
                        verbose_name="Профиль",
                    ),
                ),
            ],
            options={
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранные",
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "pk_id",
                    models.BigAutoField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Последнее обновление"
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Название")),
                (
                    "type",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[("invoice", "invoice")],
                        default=src.other.enums.DocumentType["INVOICE"],
                        enum_class=src.other.enums.DocumentType,
                        max_length=7,
                        verbose_name="Тип",
                    ),
                ),
                ("file", models.FileField(upload_to="documents/", verbose_name="Файл")),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="orders.order",
                        verbose_name="Заказ",
                    ),
                ),
            ],
            options={
                "verbose_name": "Документ Заказа",
                "verbose_name_plural": "Документы Заказов",
            },
        ),
        migrations.CreateModel(
            name="Basket",
            fields=[
                (
                    "pk_id",
                    models.BigAutoField(
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Последнее обновление"
                    ),
                ),
                (
                    "products",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Товар корзины"
                    ),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="basket",
                        to="profiles.profile",
                        verbose_name="Профиль",
                    ),
                ),
            ],
            options={
                "verbose_name": "Корзина",
                "verbose_name_plural": "Корзины",
            },
        ),
    ]

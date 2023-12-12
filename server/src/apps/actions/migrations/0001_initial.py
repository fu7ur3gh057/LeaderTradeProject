# Generated by Django 4.2.6 on 2023-12-12 09:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import src.other.enums


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("catalog", "0002_alter_brand_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="CallRequest",
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
                    "phone_number",
                    models.CharField(
                        max_length=17,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "status",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[("Продукты", "Продукты"), ("Рассрочка", "Рассрочка")],
                        default=src.other.enums.CallRequestStatus["PRODUCT"],
                        enum_class=src.other.enums.CallRequestStatus,
                        max_length=9,
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запрос Звонка",
                "verbose_name_plural": "Запросы Звонков",
            },
        ),
        migrations.CreateModel(
            name="FormApplication",
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
                    "phone_number",
                    models.CharField(
                        max_length=17,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "status",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[
                            ("Новый", "Новый"),
                            ("В прогрессе", "В прогрессе"),
                            ("Завершен", "Завершен"),
                        ],
                        default=src.other.enums.FormApplicationStatus["NEW"],
                        enum_class=src.other.enums.FormApplicationStatus,
                        max_length=11,
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "Форма Заявки",
                "verbose_name_plural": "Формы Заявки",
            },
        ),
        migrations.CreateModel(
            name="Portfolio",
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
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=250,
                        null=True,
                        unique=True,
                        verbose_name="URL путь",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="portfolios/",
                        verbose_name="Основное Изображение",
                    ),
                ),
                ("description", models.TextField()),
                (
                    "make",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolios",
                        to="catalog.make",
                        verbose_name="Марка",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolios",
                        to="products.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Портфолио",
                "verbose_name_plural": "Портфолио",
            },
        ),
        migrations.CreateModel(
            name="Review",
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
                    "client_name",
                    models.CharField(max_length=255, verbose_name="Имя клиента"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="reviews/",
                        verbose_name="Изображение",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                ("date", models.DateTimeField(verbose_name="Дата")),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.CreateModel(
            name="PortfolioImage",
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
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="portfolios/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "portfolio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery",
                        to="actions.portfolio",
                        verbose_name="Портфолио",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение Портфолио",
                "verbose_name_plural": "Изображения Портфолио",
            },
        ),
    ]
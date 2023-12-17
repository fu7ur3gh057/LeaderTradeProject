# Generated by Django 4.2.6 on 2023-12-17 12:04

from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import mptt.fields
import src.other.enums


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("title", models.CharField(max_length=255, verbose_name="Название")),
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
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="products.category",
                        verbose_name="Родитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
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
                    "season",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Сезонность"
                    ),
                ),
                ("spikes", models.BooleanField(default=False, verbose_name="Шипы")),
                (
                    "height",
                    models.IntegerField(
                        blank=True, default=0, null=True, verbose_name="Высота"
                    ),
                ),
                (
                    "diameter",
                    models.IntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Диаметр (размер)",
                    ),
                ),
                ("suv", models.BooleanField(default=False)),
                (
                    "load_index",
                    models.CharField(
                        blank=True,
                        default="-",
                        max_length=255,
                        null=True,
                        verbose_name="Индекс нагрузки",
                    ),
                ),
                (
                    "speed_index",
                    models.CharField(
                        blank=True,
                        default="-",
                        max_length=255,
                        null=True,
                        verbose_name="Индекс скорости",
                    ),
                ),
                (
                    "runflat",
                    models.BooleanField(default=False, verbose_name="Run Flat"),
                ),
                (
                    "type",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[
                            ("Диски", "Диски"),
                            ("Шины", "Шины"),
                            ("Аксессуары", "Аксессуары"),
                        ],
                        default=src.other.enums.ProductType["RIMS"],
                        enum_class=src.other.enums.ProductType,
                        max_length=10,
                        verbose_name="Тип товара",
                    ),
                ),
                (
                    "rim_type",
                    django_enum_choices.fields.EnumChoiceField(
                        blank=True,
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[("0", "0"), ("1", "1"), ("2", "2"), ("3", "3")],
                        default=None,
                        enum_class=src.other.enums.RimType,
                        max_length=1,
                        null=True,
                        verbose_name="Тип дисков",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Цвет"
                    ),
                ),
                (
                    "size",
                    models.SmallIntegerField(
                        blank=True, null=True, verbose_name="Диаметр (размер)"
                    ),
                ),
                (
                    "et",
                    models.IntegerField(blank=True, null=True, verbose_name="Вылет ET"),
                ),
                (
                    "width",
                    models.FloatField(
                        default=0, null=True, verbose_name="Ширина обода"
                    ),
                ),
                (
                    "width2",
                    models.FloatField(
                        default=0, null=True, verbose_name="Ширина обода 2"
                    ),
                ),
                ("et2", models.IntegerField(default=0, verbose_name="Вылет ET 2")),
                (
                    "dia",
                    models.FloatField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Диаметр центр. отверстия, DIA",
                    ),
                ),
                (
                    "pcd",
                    models.FloatField(
                        blank=True, default=0, null=True, verbose_name="Сверловка, PCD"
                    ),
                ),
                (
                    "bolts",
                    models.SmallIntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Количество болтов",
                    ),
                ),
                (
                    "pcd2",
                    models.FloatField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Сверловка, PCD 2",
                    ),
                ),
                (
                    "bolts2",
                    models.SmallIntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Количество болтов 2",
                    ),
                ),
                (
                    "unite_pcd",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Сверловка, PCD",
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Модель"
                    ),
                ),
                (
                    "current_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        max_digits=12,
                        null=True,
                        verbose_name="Текущая Стоимость",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        max_digits=12,
                        null=True,
                        verbose_name="Стоимость",
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        default=0,
                        max_digits=12,
                        verbose_name="Скидка",
                    ),
                ),
                (
                    "bar_code",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Код(Артикул)"
                    ),
                ),
                ("views", models.IntegerField(default=0, verbose_name="Просмотры")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="products/",
                        verbose_name="Изображение",
                    ),
                ),
                ("rest", models.IntegerField(default=0, verbose_name="Остаток")),
                (
                    "ext_data",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Дополнительная информация"
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="catalog.brand",
                        verbose_name="Производитель",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="products.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                        upload_to="products/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="album",
                        to="products.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение Товара",
                "verbose_name_plural": "Изображения Товара",
            },
        ),
    ]

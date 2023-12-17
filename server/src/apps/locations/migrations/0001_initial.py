# Generated by Django 4.2.6 on 2023-12-17 12:04

from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import src.other.enums


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("street", models.CharField(max_length=100, verbose_name="Улица")),
                ("house", models.CharField(max_length=100, verbose_name="Дом")),
                (
                    "apartment",
                    models.CharField(max_length=100, verbose_name="Квартира"),
                ),
            ],
            options={
                "verbose_name": "Адрес",
                "verbose_name_plural": "Адресы",
            },
        ),
        migrations.CreateModel(
            name="City",
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
            ],
            options={
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
            },
        ),
        migrations.CreateModel(
            name="Shop",
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
                ("email", models.CharField(max_length=255, verbose_name="Почта")),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=16,
                        max_digits=22,
                        null=True,
                        verbose_name="Широта",
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=16,
                        max_digits=22,
                        null=True,
                        verbose_name="Долгота",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shops",
                        to="locations.address",
                        verbose_name="Адрес",
                    ),
                ),
            ],
            options={
                "verbose_name": "Магазин",
                "verbose_name_plural": "Магазины",
            },
        ),
        migrations.CreateModel(
            name="Worktime",
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
                    "day_of_week",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[
                            ("Понедельник", "Понедельник"),
                            ("Вторник", "Вторник"),
                            ("Среда", "Среда"),
                            ("Четверг", "Четверг"),
                            ("Пятница", "Пятница"),
                            ("Суббота", "Суббота"),
                            ("Воскресенье", "Воскресенье"),
                        ],
                        default=src.other.enums.DayOfWeek["MONDAY"],
                        enum_class=src.other.enums.DayOfWeek,
                        max_length=11,
                        verbose_name="День недели",
                    ),
                ),
                ("start_time", models.TimeField(verbose_name="Время начала работы")),
                ("end_time", models.TimeField(verbose_name="Время завершения работы")),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="work_times",
                        to="locations.shop",
                        verbose_name="Магазин",
                    ),
                ),
            ],
            options={
                "verbose_name": "Время Работы",
                "verbose_name_plural": "Время Работы",
            },
        ),
        migrations.AddField(
            model_name="address",
            name="city",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="addresses",
                to="locations.city",
                verbose_name="Город",
            ),
        ),
    ]

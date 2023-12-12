# Generated by Django 4.2.6 on 2023-12-12 10:40

from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import src.other.enums


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("django_celery_beat", "0018_improve_crontab_helptext"),
    ]

    operations = [
        migrations.CreateModel(
            name="Unload",
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
                ("title", models.CharField(max_length=70, verbose_name="Название")),
                (
                    "service",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[("FORTOCHKI", "FORTOCHKI"), ("STARCO", "STARCO")],
                        default=src.other.enums.UnloadServiceType["fortochki"],
                        enum_class=src.other.enums.UnloadServiceType,
                        max_length=9,
                        verbose_name="Сервис",
                    ),
                ),
                (
                    "time_interval",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[
                            ("1 min", "1 min"),
                            ("5 mins", "5 mins"),
                            ("30 mins", "30 mins"),
                            ("1 hour", "1 hour"),
                            ("5 hours", "5 hours"),
                            ("12 hours", "12 hours"),
                            ("1 day", "1 day"),
                        ],
                        default=src.other.enums.TimeInterval["five_mins"],
                        enum_class=src.other.enums.TimeInterval,
                        max_length=8,
                        verbose_name="Временной интервал",
                    ),
                ),
                (
                    "status",
                    django_enum_choices.fields.EnumChoiceField(
                        choice_builder=django_enum_choices.choice_builders.value_value,
                        choices=[("Active", "Active"), ("Disabled", "Disabled")],
                        default=src.other.enums.TaskStatus["active"],
                        enum_class=src.other.enums.TaskStatus,
                        max_length=8,
                        verbose_name="Статус",
                    ),
                ),
                ("tire_unload", models.BooleanField(default=True)),
                ("rim_unload", models.BooleanField(default=True)),
                (
                    "task",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_beat.periodictask",
                        verbose_name="Периодическая задача",
                    ),
                ),
            ],
            options={
                "verbose_name": "Выгрузка",
                "verbose_name_plural": "Выгрузки",
            },
        ),
    ]
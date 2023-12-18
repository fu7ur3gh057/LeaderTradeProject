# Generated by Django 4.2.6 on 2023-12-17 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "verify_token_max_count",
                    models.IntegerField(
                        default=1,
                        help_text="Попыток верификации за токен",
                        verbose_name="Количество СМС",
                    ),
                ),
                (
                    "verify_token_generation_period",
                    models.IntegerField(
                        default=5,
                        help_text="В минутах",
                        verbose_name="Период геренации токена",
                    ),
                ),
            ],
            options={
                "verbose_name": "Настройка",
                "verbose_name_plural": "Настройки",
            },
        ),
    ]
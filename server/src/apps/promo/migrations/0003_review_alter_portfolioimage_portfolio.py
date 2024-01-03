# Generated by Django 4.2.6 on 2024-01-03 13:35

import datetime
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import promo.models


class Migration(migrations.Migration):
    dependencies = [
        ("promo", "0002_portfolio_portfolioproduct_portfolioimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
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
                ("name", models.CharField(max_length=250, verbose_name="Имя")),
                ("rating", models.IntegerField(default=5, verbose_name="Рейтинг")),
                ("content", models.TextField(verbose_name="Текст")),
                (
                    "published_at",
                    models.DateField(
                        blank=True,
                        default=datetime.date.today,
                        null=True,
                        verbose_name="Дата",
                    ),
                ),
                (
                    "pic",
                    imagekit.models.fields.ProcessedImageField(
                        blank=True,
                        null=True,
                        upload_to=promo.models.Review.get_pic_path,
                        verbose_name="фото",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.AlterField(
            model_name="portfolioimage",
            name="portfolio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pics",
                to="promo.portfolio",
            ),
        ),
    ]

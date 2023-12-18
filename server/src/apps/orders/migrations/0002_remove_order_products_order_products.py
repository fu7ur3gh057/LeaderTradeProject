# Generated by Django 4.2.6 on 2023-12-17 13:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="products",
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.JSONField(blank=True, null=True, verbose_name="Товары"),
        ),
    ]
# Generated by Django 4.2.6 on 2023-12-12 09:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="verification",
            options={
                "verbose_name": "Верификация",
                "verbose_name_plural": "Верификации",
            },
        ),
    ]
# Generated by Django 4.2.6 on 2023-12-13 13:07

from django.db import migrations
import django_enum_choices.choice_builders
import django_enum_choices.fields
import src.other.enums


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_product_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="type",
            field=django_enum_choices.fields.EnumChoiceField(
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
    ]
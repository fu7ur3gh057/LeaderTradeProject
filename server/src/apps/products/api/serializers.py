from django.utils.translation import gettext_lazy as _
from django_enum_choices.serializers import EnumChoiceField
from rest_framework import serializers

from src.apps.products.models import Category, Product
from src.other.enums import ProductType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk_id", "title", "slug"]


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj: Category):
        queryset = obj.children
        serializer = self.__class__(queryset, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ["pk_id", "title", "slug", "children"]


class ProductSerializer(serializers.ModelSerializer):
    type = EnumChoiceField(enum_class=ProductType)

    class Meta:
        model = Product
        fields = [
            "pk_id",
            "category",
            "type",
            "title",
            "slug",
            "discount",
            "current_price",
            "price",
            "color",
            "bar_code",
            "image",
            "created_at",
        ]


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["brand"]


class ProductDetailSerializer(serializers.ModelSerializer):
    type = EnumChoiceField(enum_class=ProductType)
    album = serializers.SerializerMethodField()

    def get_album(self, obj: Product) -> list[str]:
        return [img.image.url for img in obj.album.all()]

    class Meta:
        model = Product
        fields = [
            "pk_id",
            "type",
            "title",
            "slug",
            "discount",
            "price",
            "bar_code",
            "image",
            "album",
            "created_at",
            "ext_data",
        ]

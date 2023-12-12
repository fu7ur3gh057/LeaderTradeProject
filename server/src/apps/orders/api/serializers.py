from rest_framework import serializers

from src.apps.orders.models import Order, Basket, Favorites, Document


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "pk_id",
            "profile",
            "promo_code",
            "address",
            "products",
            "name",
            "surname",
            "patronymic",
            "email",
            "amount",
            "delivery",
            "status",
            "created_at",
        ]


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = [
            "pk_id",
            "profile",
            "products",
        ]


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = [
            "pk_id",
            "profile",
            "products",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

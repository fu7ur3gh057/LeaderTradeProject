from django.contrib import admin

from src.apps.orders.models import Basket, Order, Document, Favorites


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pk_id",
        "profile",
        "email",
        "address",
        "status",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["pk_id", "email", "address"]
    list_filter = ["status"]
    search_fields = ["email"]
    raw_id_fields = (
        "profile",
        "address",
        "promo_code",
    )

    def products_count(self, obj: Order) -> int:
        products: dict | None = obj.products
        if products is None:
            return 0
        return len(products)

    def products_total_count(self, obj: Order) -> int:
        pass


class DocumentAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "title", "order", "type", "created_at"]
    list_display_links = ["pk_id", "title", "order"]
    list_filter = ["type"]
    search_fields = ["title"]
    raw_id_fields = ("order",)


class BasketAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "profile", "products_count", "created_at"]
    list_display_links = ["pk_id", "profile"]
    raw_id_fields = ("profile",)

    def products_count(self, obj: Basket) -> int:
        products = obj.products
        if products is None:
            return 0
        return products.all().count()


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "profile", "products_count", "created_at"]
    list_display_links = ["pk_id", "profile"]
    raw_id_fields = (
        "profile",
        "products",
    )

    def products_count(self, obj: Favorites) -> int:
        if obj.products.all() is None:
            return 0
        return len(obj.products.all())


admin.site.register(Order, OrderAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Favorites, FavoritesAdmin)

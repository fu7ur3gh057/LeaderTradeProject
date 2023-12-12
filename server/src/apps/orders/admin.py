from django.contrib import admin

from src.apps.orders.models import Basket, Order, Document, Favorites


class OrderAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "profile", "email", "address", "status", "created_at"]
    list_display_links = ["pk_id", "email", "address"]
    list_filter = ["status"]
    search_fields = ["email"]
    raw_id_fields = (
        "profile",
        "address",
    )


class DocumentAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "title", "order", "type", "created_at"]
    list_display_links = ["pk_id", "title", "order"]
    list_filter = ["type"]
    search_fields = ["title"]
    raw_id_fields = ("order",)


class BasketAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "profile", "products_size", "created_at"]
    list_display_links = ["pk_id", "profile"]
    raw_id_fields = ("profile",)

    def products_size(self, obj: Basket):
        return len(obj.products)


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "profile", "products_size", "created_at"]
    list_display_links = ["pk_id", "profile"]
    raw_id_fields = (
        "profile",
        "products",
    )

    def products_size(self, obj: Basket):
        return len(obj.products.all())


admin.site.register(Order, OrderAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Favorites, FavoritesAdmin)

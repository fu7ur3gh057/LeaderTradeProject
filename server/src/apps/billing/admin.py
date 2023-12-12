from django.contrib import admin

from src.apps.billing.models import PromoCode


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = [
        "pk_id",
        "title",
        "code",
        "percent_discount",
        "amount_discount",
        "all_products",
        "is_active",
        "expire_time",
        "created_at",
    ]
    list_display_links = ["pk_id", "percent_discount", "amount_discount"]
    list_filter = ["is_active"]
    search_fields = ["title", "code"]
    raw_id_fields = ("products",)


admin.site.register(PromoCode, PromoCodeAdmin)

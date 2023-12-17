from django.contrib import admin

from src.apps.actions.models import (
    FormApplication,
    CallRequest,
    PortfolioImage,
    Portfolio,
    Review,
)


class PortfolioImageInline(admin.StackedInline):
    model = PortfolioImage
    extra = 1


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "make", "product", "created_at"]
    list_display_links = ["pk_id", "make", "product"]
    search_fields = ["make"]
    raw_id_fields = ("product",)
    inlines = [
        PortfolioImageInline,
    ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "client_name", "date"]
    list_display_links = ["pk_id", "client_name"]


class FormApplicationAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "phone_number", "status", "created_at"]
    list_display_links = ["pk_id", "phone_number"]


class CallRequestAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "phone_number", "status", "created_at"]
    list_display_links = ["pk_id", "phone_number"]


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FormApplication, FormApplicationAdmin)
admin.site.register(CallRequest, CallRequestAdmin)

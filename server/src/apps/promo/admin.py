from django.contrib import admin
from django.db import models
from promo.models import Promo, PortfolioImage, PortfolioProduct, Portfolio, Review
from promo.widgets import AdminImageWidget

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
	list_display = ("title", "title2", "start", "end")

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 0
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}


class PortfolioProductInline(admin.TabularInline):
    model = PortfolioProduct
    extra = 0
    raw_id_fields = ("product",)

    def _image_preview(self, obj):
        return image_div(obj.main_pic, obj.main_pic)

    _image_preview.short_description = "Фото"
    readonly_fields = ("_image_preview",)
    fields = ("product", "sort")
    show_change_link = True
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}



@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = (PortfolioImageInline, PortfolioProductInline)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'published_at')
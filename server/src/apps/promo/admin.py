from django.contrib import admin
from promo.models import Promo

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
	list_display = ("title", "title2", "start", "end")
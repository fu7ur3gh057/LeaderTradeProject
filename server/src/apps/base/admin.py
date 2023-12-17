from django.contrib import admin

from src.apps.base.models import Settings


# Register your models here.


class SettingsAdmin(admin.ModelAdmin):
    list_display = ["verify_token_max_count", "verify_token_generation_period"]
    list_display_links = ["verify_token_max_count", "verify_token_generation_period"]


admin.site.register(Settings, SettingsAdmin)

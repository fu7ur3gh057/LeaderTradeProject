from django.contrib import admin

from src.apps.unloads.models import Unload


class UnloadAdmin(admin.ModelAdmin):
    list_display = [
        "pk_id",
        "title",
        "service",
        "time_interval",
        "status",
        "created_at",
    ]
    list_display_links = ["pk_id", "service"]


admin.site.register(Unload, UnloadAdmin)

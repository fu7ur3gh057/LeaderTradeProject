from django.contrib import admin

from src.apps.unloads.models import UnloadScheduler


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
    actions = ["delete_model"]

    def delete_model(self, request, unload_list) -> None:
        for unload in unload_list:
            unload.terminate()
            unload.delete()
        print("Deleted unload")


admin.site.register(UnloadScheduler, UnloadAdmin)

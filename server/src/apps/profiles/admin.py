from django.contrib import admin

from src.apps.profiles.models import Profile, LegalCard


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "user", "email", "full_name", "is_legal", "created_at"]
    list_display_links = ["pk_id", "user", "email"]
    list_filter = ["is_legal"]
    search_fields = ["email", "full_name"]


class LegalCardAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "profile", "title", "email", "legal_address", "created_at"]
    list_display_links = ["pk_id", "email"]
    search_fields = ["email", "title"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(LegalCard, LegalCardAdmin)

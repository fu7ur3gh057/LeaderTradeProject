from django.contrib import admin

from src.apps.news.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "title", "created_at"]
    list_display_links = ["pk_id"]
    search_fields = ["title"]


admin.site.register(Post, PostAdmin)

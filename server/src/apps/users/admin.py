from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Verification


class UserAdmin(BaseUserAdmin):
    ordering = ["created_at"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["id", "phone_number", "is_active", "created_at"]
    list_display_links = ["id", "phone_number"]
    list_filter = ["phone_number", "is_active"]
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "phone_number",
                    "password",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_legal",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                )
            },
        ),
        (_("Important Dates and Codes"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    search_fields = ["phone_number"]


class VerificationAdmin(admin.ModelAdmin):
    list_display = ["pk_id", "user", "token", "attempt_count", "expire_date"]
    list_display_links = ["pk_id", "user"]
    raw_id_fields = ("user",)


admin.site.register(User, UserAdmin)
admin.site.register(Verification, VerificationAdmin)

"""
Django admin customization
"""

from django.contrib import admin
from unfold.admin import ModelAdmin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import User, Organization


class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Defines the admin pages for users."""

    ordering = ["-id"]
    list_display = [
        "id",
        "uid",
        "email",
        "first_name",
        "last_name",
        "kind",
        "status",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "image",
                    "kind",
                    "gender",
                    "status",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "organization",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "image",
                    "kind",
                    "gender",
                    "status",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    exclude = ["password1", "password2"]


admin.site.register(User, UserAdmin)


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    """Defines the admin pages for organizations."""

    ordering = ["-id"]
    list_display = ["id", "uid", "name", "slug", "status"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "logo",
                    "slug",
                    "email",
                    "subscription",
                    "description",
                    "location",
                    "expiration_date",
                    "status",
                )
            },
        ),
    )
    readonly_fields = ["uid", "slug"]
    search_fields = ["name", "slug"]

from django.contrib import admin
from unfold.admin import ModelAdmin  # Unfold's base admin
from store.models import Store, Warehouse


@admin.register(Store)
class StoreAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "marketplace",
        "country",
        "store_status",
        "store_type",
        "is_authorized",
        "order_sync",
        "inventory_sync",
    )
    list_filter = (
        "marketplace",
        "store_status",
        "store_type",
        "is_authorized",
        "order_sync",
        "inventory_sync",
        "country",
    )
    search_fields = (
        "name",
        "shop_url",
        "country",
        "marketplace",
    )
    ordering = ("-id",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "organization",
                )
            },
        ),
        (
            "Store Info",
            {
                "fields": (
                    "store_type",
                    "store_status",
                    "marketplace",
                    "shop_url",
                    "country",
                    "max_stock",
                )
            },
        ),
        (
            "Authorization",
            {
                "fields": (
                    "auth_type",
                    "is_authorized",
                    "expires_on",
                    "access_token",
                    "refresh_token",
                    "access_token_expiry",
                    "refresh_token_expiry",
                )
            },
        ),
        (
            "Sync Settings",
            {
                "fields": (
                    "order_sync",
                    "inventory_sync",
                )
            },
        ),
        (
            "Reporting",
            {
                "fields": (
                    "report_ref",
                    "report_sorted_by",
                )
            },
        ),
        (
            "Advanced",
            {"fields": ("metadata",)},
        ),
    )
    readonly_fields = ("slug",)


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "store",
        "city",
        "country",
        "is_primary",
        "is_active",
    )
    list_filter = ("country", "is_active", "is_primary", "store")
    search_fields = ("name", "code", "city", "country")
    ordering = ("-id",)

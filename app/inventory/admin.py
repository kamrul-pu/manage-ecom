from django.contrib import admin
from unfold.admin import ModelAdmin  # Unfold admin base class

from inventory.models import Stock, InventoryRequest


@admin.register(Stock)
class StockAdmin(ModelAdmin):
    list_display = ("sku", "product", "warehouse", "stock_level", "in_open", "reserve")
    list_filter = ("warehouse",)
    search_fields = ("sku", "product__name", "product__sku")
    readonly_fields = ("uid", "created_at", "updated_at")
    list_per_page = 25
    ordering = ("-created_at",)


@admin.register(InventoryRequest)
class InventoryRequestAdmin(ModelAdmin):
    list_display = ("sku", "quantity", "request_status", "dispatch_by", "stock_procced_at")
    list_filter = ("request_status",)
    search_fields = ("sku", "dispatch_by")
    readonly_fields = ("uid", "created_at", "updated_at")
    list_per_page = 25
    ordering = ("-created_at",)

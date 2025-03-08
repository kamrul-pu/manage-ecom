from django.contrib import admin

from inventory.models import Stock, InventoryRequestStock

# Register your models here.


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "stock_level",
        "location",
    )


admin.site.register(Stock, StockAdmin)


class InventoryRequestStockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dispatch_by",
        "stock_procced_at",
    )


admin.site.register(InventoryRequestStock, InventoryRequestStockAdmin)

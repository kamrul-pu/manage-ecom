from django.contrib import admin

from inventory.models import Stock, InventoryRequest

# Register your models here.


class StockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "stock_level",
        "location",
    )


admin.site.register(Stock, StockAdmin)


class InventoryRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dispatch_by",
        "stock_procced_at",
    )


admin.site.register(InventoryRequest, InventoryRequestAdmin)

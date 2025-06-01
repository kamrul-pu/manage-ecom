from django.contrib import admin
from unfold.admin import ModelAdmin

from product.models import Product, MarketplaceProduct, Mapping


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "sku",
        "organization",
        "selling_price",
        "purchase_price",
        "is_composite",
        "is_child",
        "stock_notification",
    )
    list_filter = (
        "organization",
        "is_composite",
        "is_child",
        "stock_notification",
    )
    search_fields = ("name", "sku", "barcode")
    autocomplete_fields = ("organization",)
    readonly_fields = ("uid",)
    ordering = ("name",)


@admin.register(MarketplaceProduct)
class MarketplaceProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "sku",
        "store",
        "marketplace",
        "price",
        "currency",
        "fbm",
    )
    list_filter = ("store", "marketplace", "fbm")
    search_fields = ("name", "sku", "marketplace_id")
    autocomplete_fields = ("store",)
    readonly_fields = ("uid",)
    ordering = ("-id",)


@admin.register(Mapping)
class MappingAdmin(ModelAdmin):
    list_display = (
        "product",
        "marketplace_product",
        "store",
        "marketplace",
    )
    list_filter = ("marketplace", "store")
    search_fields = (
        "product__name",
        "product__sku",
        "marketplace_product__name",
        "marketplace_product__sku",
    )
    autocomplete_fields = ("product", "marketplace_product", "store")
    readonly_fields = ("uid",)
    ordering = ("-created_at",)

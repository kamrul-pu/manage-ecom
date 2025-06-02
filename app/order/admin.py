from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from order.models import Order, OrderItem, ShippingAddress


class OrderItemInline(StackedInline):
    model = OrderItem
    extra = 0
    fields = (
        "sku",
        "local_sku",
        "quantity",
        "price",
        "total_amount",
        "picked_sku",
        "picked_at",
        "picked_item_type",
        "packed_sku",
        "packed_at",
        "position_item_ids",
    )
    readonly_fields = ("total_amount",)


class ShippingAddressInline(StackedInline):
    model = ShippingAddress
    extra = 0
    max_num = 1
    fields = (
        "buyer_name",
        "address1",
        "address2",
        "city",
        "state",
        "post_code",
        "country",
        "phone",
        "reference_id",
        "email",
    )


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "marketplace_order_id",
        "marketplace",
        "store",
        "payment_status",
        "dispatch_status",
        "purchase_date",
        "total",
    )
    list_filter = ("marketplace", "payment_status", "dispatch_status", "store")
    search_fields = ("marketplace_order_id", "store__name", "order_items__sku")
    inlines = [OrderItemInline, ShippingAddressInline]
    readonly_fields = ("total",)


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ("sku", "order", "quantity", "price", "total_amount", "picked_at")
    search_fields = ("sku", "local_sku", "order__marketplace_order_id")


@admin.register(ShippingAddress)
class ShippingAddressAdmin(ModelAdmin):
    list_display = (
        "buyer_name",
        "address1",
        "city",
        "state",
        "post_code",
        "country",
        "order",
    )
    search_fields = ("buyer_name", "order__marketplace_order_id", "email")

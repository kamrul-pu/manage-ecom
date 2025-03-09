from django.contrib import admin

from order.models import Order, OrderItem, OrderShippingAddress

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "channel_order_id",
        "uid",
        "payment_status",
        "market_place",
        "total",
        "dispatch_status",
    )


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "sku",
        "quantity",
        "price",
        "total_amount",
    )


admin.site.register(OrderItem, OrderItemAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "buyer_name",
        "city",
        "state",
        "phone",
        "email",
    )


admin.site.register(OrderShippingAddress, ShippingAddressAdmin)

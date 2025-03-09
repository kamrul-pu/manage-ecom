from django.utils import timezone
from rest_framework import serializers
from django.db import transaction

from order.models import Order, OrderItem, OrderShippingAddress
from order.serializers.order_items import OrderItemSerializer
from order.serializers.shipping_address import OrderShippingAddressSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)
    shipping_address = OrderShippingAddressSerializer(required=False)

    class Meta:
        model = Order
        fields = (
            "uid",
            "channel",
            "channel_order_id",
            "payment_status",
            "payment_method",
            "purchase_date",
            "currency",
            "total",
            "market_place",
            "dispatch_status",
            "dispatch_identifier",
            "dispatched_by",
            "dispatched_at",
            "shipped_at",
            "order_meta",
            "order_items",
            "shipping_address",
        )
        read_only_fields = ("uid", "total")

    def create(self, validated_data):
        """Handle nested creation with bulk operations."""
        order_items_data = validated_data.pop("order_items", [])
        shipping_address_data = validated_data.pop("shipping_address", None)

        with transaction.atomic():  # Wrap operations in a transaction
            # Create the order
            order = Order.objects.create(**validated_data)

            # Bulk create order items if any
            if order_items_data:
                order_items = [
                    OrderItem(order=order, **item_data)
                    for item_data in order_items_data
                ]
                OrderItem.objects.bulk_create(order_items)

            # Create shipping address if provided
            if shipping_address_data:
                OrderShippingAddress.objects.create(
                    order=order, **shipping_address_data
                )

        return order

    def update(self, instance, validated_data):
        """Handle nested updates with bulk operations."""
        order_items_data = validated_data.pop("order_items", None)
        shipping_address_data = validated_data.pop("shipping_address", None)

        with transaction.atomic():  # Wrap operations in a transaction
            # Update order fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Update or create order items
            if order_items_data is not None:
                # Delete existing items
                instance.order_items.all().delete()
                # Bulk create new items
                order_items = [
                    OrderItem(order=instance, **item_data)
                    for item_data in order_items_data
                ]
                OrderItem.objects.bulk_create(order_items)

            # Update or create shipping address
            if shipping_address_data is not None:
                if hasattr(instance, "shipping_address"):
                    for attr, value in shipping_address_data.items():
                        setattr(instance.shipping_address, attr, value)
                    instance.shipping_address.save()
                else:
                    OrderShippingAddress.objects.create(
                        order=instance, **shipping_address_data
                    )

        return instance

    def validate_purchase_date(self, value):
        """Ensure purchase_date is not in the future."""
        if value > timezone.now():
            raise serializers.ValidationError("Purchase date cannot be in the future.")
        return value

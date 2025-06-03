from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers

from order.choices import DispatchStatus
from order.models import Order, OrderItem, ShippingAddress
from order.serializers.order_items import OrderItemSerializer
from order.serializers.shipping_address import ShippingAddressSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)
    shipping_address = ShippingAddressSerializer(required=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "uid",
            "store",
            "marketplace_order_id",
            "payment_status",
            "payment_method",
            "purchase_date",
            "currency",
            "total",
            "marketplace",
            "dispatch_status",
            "dispatch_identifier",
            "dispatched_by",
            "dispatched_at",
            "shipped_at",
            "order_meta",
            "order_items",
            "shipping_address",
        )
        read_only_fields = ("id", "uid", "total")

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items", [])
        shipping_address_data = validated_data.pop("shipping_address", None)

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            total = Decimal("0.00")
            if order_items_data:
                order_items = []
                for item_data in order_items_data:
                    total_amount = item_data["price"] * item_data["quantity"]
                    item_data["total_amount"] = total_amount
                    order_items.append(OrderItem(order=order, **item_data))
                    total += total_amount
                OrderItem.objects.bulk_create(order_items)

            order.total = total
            order.save()

            if shipping_address_data:
                ShippingAddress.objects.create(order=order, **shipping_address_data)

        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("order_items", None)
        shipping_address_data = validated_data.pop("shipping_address", None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if order_items_data is not None:
                instance.order_items.all().delete()
                total = Decimal("0.00")
                order_items = []
                for item_data in order_items_data:
                    total_amount = item_data["price"] * item_data["quantity"]
                    item_data["total_amount"] = total_amount
                    order_items.append(OrderItem(order=instance, **item_data))
                    total += total_amount
                OrderItem.objects.bulk_create(order_items)
                instance.total = total
                instance.save()

            if shipping_address_data is not None:
                if hasattr(instance, "shipping_address"):
                    for attr, value in shipping_address_data.items():
                        setattr(instance.shipping_address, attr, value)
                    instance.shipping_address.save()
                else:
                    ShippingAddress.objects.create(
                        order=instance, **shipping_address_data
                    )

        return instance

    def validate_purchase_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Purchase date cannot be in the future.")
        return value


class OrderStatusUpdateSerializer(serializers.Serializer):
    order_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    dispatch_status = serializers.ChoiceField(choices=DispatchStatus.choices)

from rest_framework import serializers
from order.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "uid",
            "sku",
            "quantity",
            "price",
            "total_amount",
            "position_item_ids",
            "picked_sku",
            "picked_at",
            "picked_item_type",
            "packed_sku",
            "packed_at",
        )
        read_only_fields = ("uid", "total_amount")

    def validate(self, attrs):
        """Ensure price and quantity are positive for total_amount calculation."""
        price = attrs.get("price", self.instance.price if self.instance else None)
        quantity = attrs.get(
            "quantity", self.instance.quantity if self.instance else None
        )
        if price is not None and price < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        if quantity is not None and quantity < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return attrs

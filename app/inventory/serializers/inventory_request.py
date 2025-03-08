from rest_framework import serializers
from inventory.models import InventoryRequestStock, Stock


from inventory.serializers.stock import StockSerializer


class InventoryRequestStockSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.filter(), source="stock", write_only=True
    )

    class Meta:
        model = InventoryRequestStock
        fields = [
            "id",  # From BaseModelWithUID
            "stock",
            "stock_id",  # For writing
            "data",
            "request_status",
            "location",
            "batch_metadata",
            "dispatch_by",
            "stock_procced_at",
            "created_at",  # From BaseModelWithUID
            "updated_at",  # From BaseModelWithUID
        ]
        read_only_fields = ("id", "created_at", "updated_at")

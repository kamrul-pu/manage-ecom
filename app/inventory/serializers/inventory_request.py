from rest_framework import serializers
from inventory.models import InventoryRequest, Stock


from inventory.serializers.stock import StockListSerializer


class InventoryRequestSerializer(serializers.ModelSerializer):
    stock = StockListSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.filter(), source="stock", write_only=True
    )

    class Meta:
        model = InventoryRequest
        fields = [
            "id",
            "uid",
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

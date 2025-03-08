from rest_framework import serializers
from inventory.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",  # From BaseModelWithUID
            "local_product",
            "stock_level",
            "in_open",
            "minimum_quantity",
            "location",
            "created_at",  # From BaseModelWithUID
            "updated_at",  # From BaseModelWithUID
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

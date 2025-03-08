from rest_framework import serializers
from inventory.models import Stock
from product.serializers.product import ProductBase


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "id",
            "uid",
            "product",
            "stock_level",
            "in_open",
            "minimum_quantity",
            "location",
        )
        read_only_fields = (
            "id",
            "uid",
        )


class StockDetailSerializer(StockListSerializer):
    product = ProductBase(read_only=True)

    class Meta(StockListSerializer.Meta):
        fields = StockListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )

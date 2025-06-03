from rest_framework import serializers
from inventory.models import Stock

from product.serializers.product import ProductBase


class StockBase(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "id",
            "uid",
            "sku",
            "product",
            "stock_level",
            "in_open",
            "available",
            "minimum_quantity",
            "reserve",
            "warehouse",
        )
        read_only_fields = (
            "id",
            "uid",
        )


class StockListSerializer(StockBase):
    class Meta(StockBase.Meta):
        fields = StockBase.Meta.fields + ()
        read_only_fields = StockBase.Meta.read_only_fields + ()


class StockDetailSerializer(StockListSerializer):
    product = ProductBase(read_only=True)

    class Meta(StockListSerializer.Meta):
        fields = StockListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )

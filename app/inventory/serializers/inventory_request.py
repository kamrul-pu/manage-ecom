from rest_framework import serializers
from inventory.models import InventoryRequest


class InventoryRequestBase(serializers.ModelSerializer):
    class Meta:
        model = InventoryRequest
        fields = (
            "id",
            "uid",
            "sku",
            "quantity",
            "metadata",
            "request_status",
            "dispatch_by",
            "stock_procced_at",
        )
        read_only_fields = (
            "id",
            "uid",
        )


class InventoryRequestListSerializer(InventoryRequestBase):
    class Meta(InventoryRequestBase.Meta):
        fields = InventoryRequestBase.Meta.fields + ()

        read_only_fields = InventoryRequestBase.Meta.read_only_fields + ()


class InventoryRequestDetailSerializer(InventoryRequestListSerializer):
    class Meta(InventoryRequestListSerializer.Meta):
        fields = InventoryRequestListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = InventoryRequestListSerializer.Meta.read_only_fields + (
            "created_at",
            "updated_at",
        )

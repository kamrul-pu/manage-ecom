from rest_framework import serializers
from store.models import Warehouse
from store.serializers.store import StoreBaseSerializer  # If you want nested store info


class WarehouseBase(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "code",
            "store",
            "is_primary",
            "is_active",
            "city",
            "country",
        )
        read_only_fields = ("id", "uid", "slug")


class WarehouseListSerializer(WarehouseBase):

    class Meta(WarehouseBase.Meta):
        fields = WarehouseBase.Meta.fields + (
            "address_line1",
            "address_line2",
            "state",
            "postal_code",
            "contact_name",
            "contact_phone",
            "description",
        )
        read_only_fields = WarehouseBase.Meta.read_only_fields + ()


class WarehouseDetailSerializer(WarehouseListSerializer):
    store = StoreBaseSerializer(read_only=True)

    class Meta(WarehouseListSerializer.Meta):
        fields = WarehouseListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = WarehouseListSerializer.Meta.read_only_fields + (
            "created_at",
            "updated_at",
        )

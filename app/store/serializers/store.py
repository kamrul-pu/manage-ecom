from rest_framework import serializers

from core.serializers.organization import OrganizationBase

from store.models import Store


class StoreBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "organization",
            "store_status",
            "store_type",
            "shop_url",
            "marketplace",
            "country",
            "description",
        )
        read_only_fields = (
            "id",
            "uid",
            "slug",
        )


class StoreListSerializer(StoreBaseSerializer):
    class Meta(StoreBaseSerializer.Meta):
        fields = StoreBaseSerializer.Meta.fields + (
            "is_authorized",
            "expires_on",
            "order_sync",
            "inventory_sync",
            "max_stock",
            "metadata",  # was 'store_metadata' in the previous version
            "auth_type",
            "access_token_expiry",
            "refresh_token_expiry",
        )
        read_only_fields = StoreBaseSerializer.Meta.read_only_fields


class StoreDetailSerializer(StoreListSerializer):
    organization = OrganizationBase(read_only=True)

    class Meta(StoreListSerializer.Meta):
        fields = StoreListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
            "access_token",
            "refresh_token",
            "report_ref",
            "report_sorted_by",
        )
        read_only_fields = StoreListSerializer.Meta.read_only_fields

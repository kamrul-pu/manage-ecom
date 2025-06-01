from rest_framework.serializers import ModelSerializer
from product.models import MarketplaceProduct
from store.serializers.store import StoreBaseSerializer  # Adjust if path is different


class MarketplaceProductBase(ModelSerializer):
    class Meta:
        model = MarketplaceProduct
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "store",
            "marketplace_id",
            "marketplace",
            "sku",
            "category",
            "image",
            "url",
            "fbm",
            "price",
            "currency",
        )
        read_only_fields = (
            "id",
            "uid",
            "slug",
        )


class MarketplaceProductListSerializer(MarketplaceProductBase):
    class Meta(MarketplaceProductBase.Meta):
        fields = MarketplaceProductBase.Meta.fields + ("metadata",)
        read_only_fields = MarketplaceProductBase.Meta.read_only_fields


class MarketplaceProductDetailSerializer(MarketplaceProductListSerializer):
    store = StoreBaseSerializer(read_only=True)

    class Meta(MarketplaceProductListSerializer.Meta):
        fields = MarketplaceProductListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = MarketplaceProductListSerializer.Meta.read_only_fields + (
            "created_at",
            "updated_at",
        )

from rest_framework.serializers import ModelSerializer
from product.models import Mapping
from product.serializers.product import ProductBase
from product.serializers.marketplace_product import MarketplaceProductBase
from store.serializers.store import StoreBaseSerializer  # Adjust if needed


class MappingBase(ModelSerializer):
    class Meta:
        model = Mapping
        fields = (
            "id",
            "uid",
            "product",
            "marketplace_product",
            "store",
            "marketplace",
        )
        read_only_fields = (
            "id",
            "uid",
        )


class MappingListSerializer(MappingBase):
    product = ProductBase(read_only=True)
    marketplace_product = MarketplaceProductBase(read_only=True)
    store = StoreBaseSerializer(read_only=True)

    class Meta(MappingBase.Meta):
        fields = MappingBase.Meta.fields + ()


class MappingDetailSerializer(MappingListSerializer):
    class Meta(MappingListSerializer.Meta):
        fields = MappingListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = MappingListSerializer.Meta.read_only_fields + (
            "created_at",
            "updated_at",
        )

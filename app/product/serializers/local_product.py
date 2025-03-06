from rest_framework.serializers import ModelSerializer
from product.models import LocalProduct


class LocalProductBase(ModelSerializer):
    class Meta:
        model = LocalProduct
        fields = (
            "id",
            "uid",
            "name",
            "channel",
            "slug",
            "sku",
            "barcode",
            "description",
            "selling_price",
            "purchase_price",
            "image",
            "width",
            "height",
            "weight",
            "depth",
        )
        read_only_fields = (
            "id",
            "uid",
            "slug",
        )


class LocalProductListSerializer(LocalProductBase):
    class Meta(LocalProductBase.Meta):
        fields = LocalProductBase.Meta.fields + (
            "is_composite",
            "is_child",
            "stock_notification",
        )
        read_only_fields = LocalProductBase.Meta.read_only_fields + ()


class LocalProductDetailSerializer(LocalProductListSerializer):
    class Meta(LocalProductListSerializer.Meta):
        fields = LocalProductListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = LocalProductListSerializer.Meta.read_only_fields + ()

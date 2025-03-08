from rest_framework.serializers import ModelSerializer
from product.models import Product


class ProductBase(ModelSerializer):
    class Meta:
        model = Product
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


class ProductListSerializer(ProductBase):
    class Meta(ProductBase.Meta):
        fields = ProductBase.Meta.fields + (
            "is_composite",
            "is_child",
            "stock_notification",
        )
        read_only_fields = ProductBase.Meta.read_only_fields + ()


class ProductDetailSerializer(ProductListSerializer):
    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = ProductListSerializer.Meta.read_only_fields + ()

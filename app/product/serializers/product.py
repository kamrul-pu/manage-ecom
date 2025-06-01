from rest_framework.serializers import ModelSerializer
from product.models import Product
from core.serializers.organization import OrganizationBase


class ProductBase(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "organization",  # changed from "channel" to "store"
            "sku",
            "barcode",
            "description",
            "selling_price",
            "selling_currency",
            "purchase_price",
            "purchase_currency",
            "style",
            "color",
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
            "metadata",
        )
        read_only_fields = ProductBase.Meta.read_only_fields + ()


class ProductDetailSerializer(ProductListSerializer):
    organization = OrganizationBase(required=False)  # updated field

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = ProductListSerializer.Meta.read_only_fields + ()

from rest_framework.serializers import ModelSerializer
from product.models import RemoteProduct


class RemoteProductBase(ModelSerializer):
    class Meta:
        model = RemoteProduct
        fields = (
            "id",
            "uid",
            "local_product",
            "name",
            "slug",
            "sku",
            "description",
            "fba_status",
        )
        read_only_fields = (
            "id",
            "uid",
            "slug",
        )


class RemoteProductListSerializer(RemoteProductBase):
    class Meta(RemoteProductBase.Meta):
        fields = RemoteProductBase.Meta.fields + ()
        read_only_fields = RemoteProductBase.Meta.read_only_fields + ()


class RemoteProductDetailSerializer(RemoteProductListSerializer):
    class Meta(RemoteProductListSerializer.Meta):
        fields = RemoteProductListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = RemoteProductListSerializer.Meta.read_only_fields + ()

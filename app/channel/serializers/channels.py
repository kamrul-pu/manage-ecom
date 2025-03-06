from rest_framework.serializers import ModelSerializer

from channel.models import Channel


class ChannelBaseSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "company",
            "channel_state",
            "channel_type",
            "shop_url",
            "country",
            "description",
        )
        read_only_fields = (
            "id",
            "uid",
            "slug",
        )


class ChannelListSerializer(ChannelBaseSerializer):
    class Meta(ChannelBaseSerializer.Meta):
        fields = ChannelBaseSerializer.Meta.fields + (
            "is_authorized",
            "expires_on",
            "channel_metadata",
            "order_sync",
            "inventory_sync",
            "channel_max_stock",
        )
        read_only_fields = ChannelBaseSerializer.Meta.read_only_fields + ()


class ChannelDetailSerializer(ChannelListSerializer):
    class Meta(ChannelListSerializer.Meta):
        fields = ChannelListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = ChannelListSerializer.Meta.read_only_fields + ()

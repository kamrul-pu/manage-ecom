from rest_framework import serializers

from core.serializers.user import UserListSerializer

from channel.models import Channel


class ChannelBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "user",
            "channel_state",
            "channel_type",
            "shop_url",
            "market_place",
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
    user = UserListSerializer(read_only=True)

    class Meta(ChannelListSerializer.Meta):
        fields = ChannelListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = ChannelListSerializer.Meta.read_only_fields + ()

from rest_framework import serializers

from order.models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = (
            "uid",
            "buyer_name",
            "address1",
            "address2",
            "city",
            "state",
            "post_code",
            "country",
            "phone",
            "reference_id",
            "email",
        )
        read_only_fields = ("uid",)

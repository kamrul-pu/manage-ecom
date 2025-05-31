from rest_framework.serializers import ModelSerializer

from core.models import Organization


class OrganizationBase(ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "uid",
            "name",
            "email",
            "location",
            "slug",
            "logo",
        )
        read_only_fields = (
            "id",
            "uid",
            "slug",
        )


class OrganizationListSerializer(OrganizationBase):
    class Meta(OrganizationBase.Meta):
        fields = OrganizationBase.Meta.fields + (
            "description",
            "location",
            "expiration_date",
        )
        read_only_fields = OrganizationBase.Meta.read_only_fields + ()


class OrganizationDetailSerializer(OrganizationListSerializer):
    class Meta(OrganizationListSerializer.Meta):
        fields = OrganizationListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
        read_only_fields = OrganizationListSerializer.Meta.read_only_fields + ()

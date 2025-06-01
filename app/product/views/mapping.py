from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from product.models import Mapping
from product.serializers.mapping import (
    MappingListSerializer,
    MappingDetailSerializer,
)


class MappingList(ListCreateAPIView):
    queryset = Mapping().get_all_actives()
    serializer_class = MappingListSerializer
    permission_classes = (AllowAny,)


class MappingDetail(RetrieveUpdateDestroyAPIView):
    queryset = (
        Mapping()
        .get_all_actives()
        .select_related("product", "marketplace_product", "store")
    )
    serializer_class = MappingDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

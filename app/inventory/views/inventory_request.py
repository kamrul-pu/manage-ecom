from rest_framework import generics
from rest_framework.permissions import AllowAny

from inventory.models import InventoryRequest
from inventory.serializers.inventory_request import (
    InventoryRequestListSerializer,
    InventoryRequestDetailSerializer,
)


# InventoryRequestStock Views
class InventoryRequestList(generics.ListCreateAPIView):
    serializer_class = InventoryRequestListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = InventoryRequest().get_all_actives()
        sku = self.request.query_params.get("sku", None)
        if sku:
            queryset = queryset.filter(sku=sku)
        return queryset


class InventoryRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryRequest().get_all_actives()
    serializer_class = InventoryRequestDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

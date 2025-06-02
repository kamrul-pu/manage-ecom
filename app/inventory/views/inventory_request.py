from rest_framework import generics
from rest_framework.permissions import AllowAny

from inventory.models import InventoryRequest
from inventory.serializers.inventory_request import InventoryRequestListSerializer, InventoryRequestDetailSerializer


# InventoryRequestStock Views
class InventoryRequestList(generics.ListCreateAPIView):
    queryset = InventoryRequest().get_all_actives()
    serializer_class = InventoryRequestListSerializer
    permission_classes = (AllowAny,)


class InventoryRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryRequest().get_all_actives()
    serializer_class = InventoryRequestDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

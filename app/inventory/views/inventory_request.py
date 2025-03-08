from rest_framework import generics
from rest_framework.permissions import AllowAny

from inventory.models import InventoryRequestStock
from inventory.serializers.inventory_request import InventoryRequestStockSerializer


# InventoryRequestStock Views
class InventoryRequestStockList(generics.ListCreateAPIView):
    queryset = InventoryRequestStock().get_all_actives()
    serializer_class = InventoryRequestStockSerializer
    permission_classes = (AllowAny,)


class InventoryRequestStockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryRequestStock().get_all_actives()
    serializer_class = InventoryRequestStockSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

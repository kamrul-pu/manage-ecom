from rest_framework import generics
from rest_framework.permissions import AllowAny

from inventory.models import InventoryRequest
from inventory.serializers.inventory_request import InventoryRequestSerializer


# InventoryRequestStock Views
class InventoryRequestList(generics.ListCreateAPIView):
    queryset = InventoryRequest().get_all_actives().select_related("stock")
    serializer_class = InventoryRequestSerializer
    permission_classes = (AllowAny,)


class InventoryRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryRequest().get_all_actives().select_related("stock")
    serializer_class = InventoryRequestSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

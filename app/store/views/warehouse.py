from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from store.serializers.warehouse import (
    WarehouseListSerializer,
    WarehouseDetailSerializer,
)

from store.models import Warehouse


class WarehouseList(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Warehouse().get_all_actives()
    serializer_class = WarehouseListSerializer


class WarehouseDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Warehouse().get_all_actives().select_related("store")
    serializer_class = WarehouseDetailSerializer
    lookup_field = "uid"

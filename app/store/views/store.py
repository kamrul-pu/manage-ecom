from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from store.serializers.store import StoreListSerializer, StoreDetailSerializer
from store.serializers.warehouse import WarehouseListSerializer

from store.models import Warehouse

from store.models import Store


class StoreList(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Store().get_all_actives()
    serializer_class = StoreListSerializer


class StoreDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Store().get_all_actives().select_related("organization")
    serializer_class = StoreDetailSerializer
    lookup_field = "uid"


class StoreWareHouseList(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = WarehouseListSerializer

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        if not uid:
            return Warehouse.objects.none()
        try:
            store = Store.objects.get(uid=uid)
        except Store.DoesNotExist:
            return Warehouse.objects.none()
        queryset = Warehouse.objects.filter(store_id=store.id)
        return queryset

    def perform_create(self, serializer):
        uid = self.kwargs.get("uid")
        if not uid:
            return Response(
                {"detail": "Store UID is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            store = Store.objects.get(uid=uid)
        except Store.DoesNotExist:
            return Response(
                {"detail": "Store not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(store=store)

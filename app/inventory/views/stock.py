# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from inventory.models import Stock
from inventory.serializers.stock import StockListSerializer, StockDetailSerializer


# Stock Views
class StockList(generics.ListCreateAPIView):
    serializer_class = StockListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Stock().get_all_actives()
        sku = self.request.query_params.get("sku", None)
        warehouse_code = self.request.query_params.get("warehouse_code", None)
        if warehouse_code:
            queryset = queryset.filter(warehouse__code=warehouse_code)
        if sku:
            queryset = queryset.filter(product__sku=sku)
        return queryset


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock().get_all_actives().select_related("product")
    serializer_class = StockDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

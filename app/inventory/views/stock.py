# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from inventory.models import Stock
from inventory.serializers.stock import StockListSerializer, StockDetailSerializer


# Stock Views
class StockList(generics.ListCreateAPIView):
    queryset = Stock().get_all_actives()
    serializer_class = StockListSerializer
    permission_classes = (AllowAny,)


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock().get_all_actives().select_related("product")
    serializer_class = StockDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

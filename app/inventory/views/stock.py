# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from inventory.models import Stock
from inventory.serializers.stock import StockSerializer


# Stock Views
class StockList(generics.ListCreateAPIView):
    queryset = Stock().get_all_actives()
    serializer_class = StockSerializer
    permission_classes = (AllowAny,)


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock().get_all_actives()
    serializer_class = StockSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

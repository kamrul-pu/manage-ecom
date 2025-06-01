from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from product.models import MarketplaceProduct

from product.serializers.marketplace_product import (
    MarketplaceProductListSerializer,
    MarketplaceProductDetailSerializer,
)


class MarketplaceProductList(ListCreateAPIView):
    queryset = MarketplaceProduct().get_all_actives()
    serializer_class = MarketplaceProductListSerializer
    permission_classes = (AllowAny,)


class MarketplaceProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = MarketplaceProduct().get_all_actives().select_related("store")
    serializer_class = MarketplaceProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

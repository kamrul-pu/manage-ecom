from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from product.serializers.product import (
    ProductListSerializer,
    ProductDetailSerializer,
)


from product.models import Product


class ProductList(ListCreateAPIView):
    queryset = Product().get_all_actives()
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product().get_all_actives()
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

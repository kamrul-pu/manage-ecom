from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from product.serializers.local_product import (
    LocalProductListSerializer,
    LocalProductDetailSerializer,
)


from product.models import LocalProduct


class LocalProductList(ListCreateAPIView):
    queryset = LocalProduct().get_all_actives()
    serializer_class = LocalProductListSerializer
    permission_classes = (AllowAny,)


class LocalProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = LocalProduct().get_all_actives()
    serializer_class = LocalProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

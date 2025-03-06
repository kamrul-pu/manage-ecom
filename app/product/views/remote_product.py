from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from product.serializers.remote_product import (
    RemoteProductListSerializer,
    RemoteProductDetailSerializer,
)


from product.models import RemoteProduct


class RemoteProductList(ListCreateAPIView):
    queryset = RemoteProduct().get_all_actives()
    serializer_class = RemoteProductListSerializer
    permission_classes = (AllowAny,)


class RemoteProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = RemoteProduct().get_all_actives()
    serializer_class = RemoteProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

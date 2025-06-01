from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from product.serializers.product import (
    ProductListSerializer,
    ProductDetailSerializer,
)

from product.serializers.mapping import MappingListSerializer


from product.models import Product, Mapping


class ProductList(ListCreateAPIView):
    queryset = Product().get_all_actives()
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product().get_all_actives().select_related("organization")
    serializer_class = ProductDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"


class ProductMappingList(ListCreateAPIView):
    queryset = Mapping().get_all_actives()
    serializer_class = MappingListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        if not uid:
            return Mapping.objects.none()
        try:
            product = Product.objects.get(uid=uid)
        except Product.DoesNotExist:
            return Mapping.objects.none()
        queryset = Mapping.objects.filter(product_id=product.id)
        return queryset

    def perform_create(self, serializer):
        uid = self.kwargs.get("uid")
        if not uid:
            return Response(
                {"detail": "Product UID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product = Product.objects.get(uid=uid)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(organization=self.request.user.organization)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from order.models import Order
from order.serializers.order import OrderSerializer


class OrderList(generics.ListCreateAPIView):

    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"

    def get_queryset(self):
        queryset = (
            Order()
            .get_all_actives()
            .prefetch_related("order_items", "shipping_address")
        )
        # Optionally filter by store if provided in the request
        store_uid = self.request.query_params.get("store_uid")
        if store_uid:
            queryset = queryset.filter(store__uid=store_uid)
        # Optionally filter by marketplace if provided in the request
        marketplace = self.request.query_params.get("marketplace")
        if marketplace:
            queryset = queryset.filter(marketplace=marketplace)
        # Optionally filter by payment status if provided in the request
        payment_status = self.request.query_params.get("payment_status")
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        # Optionally filter by dispatch status if provided in the request
        dispatch_status = self.request.query_params.get("dispatch_status")
        if dispatch_status:
            queryset = queryset.filter(dispatch_status=dispatch_status)
        # Optionally filter by marketplace order ID if provided in the request
        marketplace_order_id = self.request.query_params.get("marketplace_order_id")
        if marketplace_order_id:
            queryset = queryset.filter(marketplace_order_id=marketplace_order_id)
        # Optionally filter by dispatched_by if provided in the request
        dispatched_by = self.request.query_params.get("dispatched_by")
        if dispatched_by:
            queryset = queryset.filter(dispatched_by=dispatched_by)
        # Optionally filter by dispatched_at if provided in the request
        dispatched_at = self.request.query_params.get("dispatched_at")
        if dispatched_at:
            queryset = queryset.filter(dispatched_at=dispatched_at)
        # Optionally filter by shipped_at if provided in the request
        shipped_at = self.request.query_params.get("shipped_at")
        if shipped_at:
            queryset = queryset.filter(shipped_at=shipped_at)
        # Optionally filter by purchase_date if provided in the request
        purchase_date = self.request.query_params.get("purchase_date")
        if purchase_date:
            queryset = queryset.filter(purchase_date=purchase_date)
        return queryset


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Order().get_all_actives().prefetch_related("order_items", "shipping_address")
    )
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import status
# from order.models import Order
# from order.serializers.order import OrderSerializer


# class OrderList(APIView):
#     permission_classes = (AllowAny,)

#     def get(self, request):
#         """List all orders."""
#         orders = Order.objects.filter().prefetch_related(
#             "order_items", "shipping_address"
#         )
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         """Create a new order."""
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrderDetail(APIView):
#     permission_classes = (AllowAny,)

#     def get_object(self, uid):
#         try:
#             return Order.objects.get(uid=uid)
#         except Order.DoesNotExist:
#             return None

#     def get(self, request, uid):
#         """Retrieve an order by UID."""
#         order = self.get_object(uid)
#         if not order:
#             return Response(
#                 {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)

#     def put(self, request, uid):
#         """Update an order by UID."""
#         order = self.get_object(uid)
#         if not order:
#             return Response(
#                 {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = OrderSerializer(order, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, uid):
#         """Partially update an order by UID."""
#         order = self.get_object(uid)
#         if not order:
#             return Response(
#                 {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = OrderSerializer(order, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, uid):
#         """Delete an order by UID."""
#         order = self.get_object(uid)
#         if not order:
#             return Response(
#                 {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

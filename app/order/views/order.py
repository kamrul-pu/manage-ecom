from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from order.choices import DispatchStatus
from inventory.models import Stock
from order.models import Order, OrderItem
from order.serializers.order import OrderSerializer, OrderStatusUpdateSerializer


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


def update_stock_on_status_change(order, dispatch_status):
    order_items = OrderItem.objects.filter(order=order)

    for item in order_items:
        stock = Stock.objects.filter(sku=item.local_sku).first()
        if not stock:
            print(f"Stock not found for local SKU: {item.local_sku}")
            continue

        quantity = item.quantity

        if dispatch_status in [DispatchStatus.OPEN_ORDER, DispatchStatus.PENDING]:
            stock.in_open += quantity
        elif dispatch_status == DispatchStatus.CANCELLED:
            stock.in_open = max(0, stock.in_open - quantity)
        elif dispatch_status == DispatchStatus.DISPATCHED:
            stock.in_open = max(0, stock.in_open - quantity)
            stock.stock_level = max(0, stock.stock_level - quantity)

        stock.available = max(0, stock.stock_level - stock.in_open)
        stock.save()

        print(f"✅ Stock updated for {item.local_sku} ({dispatch_status})")


class OrderStatusUpdateBulk(APIView):
    serializer_class = OrderStatusUpdateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_ids = serializer.validated_data.get("order_ids", [])
        dispatch_status = serializer.validated_data.get("dispatch_status", "OPEN_ORDER")

        # Fetch orders first (so we can update stock before changing status)
        orders = Order.objects.filter(id__in=order_ids)

        for order in orders:
            update_stock_on_status_change(order, dispatch_status)
            order.dispatch_status = dispatch_status
            order.save()

        return Response(
            {
                "message": f"{orders.count()} order(s) updated to '{dispatch_status}'.",
                "status": dispatch_status,
                "order_ids": order_ids,
            },
            status=status.HTTP_200_OK,
        )


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

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from order.models import Order
from order.serializers.order import OrderListSerializer, OrderDetailSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order().get_all_actives()
    serializer_class = OrderListSerializer
    permission_classes = (AllowAny,)
    lookup_field = "uid"


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Order().get_all_actives().prefetch_related("order_items", "shipping_address")
    )
    serializer_class = OrderDetailSerializer
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

from django.urls import path


from order.views.order import OrderList, OrderDetail, OrderStatusUpdateBulk

urlpatterns = [
    path("", OrderList.as_view(), name="order-list"),
    path("/<uuid:uid>", OrderDetail.as_view(), name="order-detail"),
    path("/update", OrderStatusUpdateBulk.as_view(), name="order-status-update"),
]

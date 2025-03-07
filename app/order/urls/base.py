from django.urls import path, include

urlpatterns = [
    path("", include("order.urls.order"), name="order-urls"),
]

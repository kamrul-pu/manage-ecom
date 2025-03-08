from django.urls import path

from inventory.views.stock import StockList, StockDetail

urlpatterns = [
    path("", StockList.as_view(), name="stock-list"),
    path("/<uuid:uid>", StockDetail.as_view(), name="stock-detail"),
]

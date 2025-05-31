from django.urls import path

from store.views.warehouse import WarehouseList, WarehouseDetail

urlpatterns = [
    path("", WarehouseList.as_view(), name="warehouse-list"),
    path("/<uuid:uid>", WarehouseDetail.as_view(), name="warehouse-detail"),
]

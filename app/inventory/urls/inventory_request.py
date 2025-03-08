from django.urls import path

from inventory.views.inventory_request import (
    InventoryRequestStockList,
    InventoryRequestStockDetail,
)


urlpatterns = [
    path("", InventoryRequestStockList.as_view(), name="inventory-request-list"),
    path(
        "/<uuid:uid>",
        InventoryRequestStockDetail.as_view(),
        name="inventory-request-detail",
    ),
]

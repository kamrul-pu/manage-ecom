from django.urls import path

from inventory.views.inventory_request import (
    InventoryRequestList,
    InventoryRequestDetail,
)


urlpatterns = [
    path("", InventoryRequestList.as_view(), name="inventory-request-list"),
    path(
        "/<uuid:uid>", InventoryRequestDetail.as_view(), name="inventory-request-detail"
    ),
]

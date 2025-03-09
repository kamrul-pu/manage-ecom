from django.urls import path, include

urlpatterns = [
    path("/stocks", include("inventory.urls.stock"), name="stock-urls"),
    path(
        "/stock-requests",
        include("inventory.urls.inventory_request"),
        name="inventory-request-urls",
    ),
]

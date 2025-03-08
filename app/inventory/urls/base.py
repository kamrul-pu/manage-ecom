from django.urls import path, include

urlpatterns = [
    path("/stock", include("inventory.urls.stock"), name="stock-urls"),
    path(
        "/stock-request",
        include("inventory.urls.inventory_request"),
        name="inventory-request-urls",
    ),
]

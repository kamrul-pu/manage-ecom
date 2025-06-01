from django.urls import path, include

urlpatterns = [
    path("", include("product.urls.product"), name="product-urls"),
    path(
        "/marketplace-products",
        include("product.urls.marketplace_product"),
        name="marketplace-product-urls",
    ),
    path("/mappings", include("product.urls.mapping"), name="mapping-urls"),
]

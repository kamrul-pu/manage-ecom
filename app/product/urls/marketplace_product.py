from django.urls import path

from product.views.marketplace_product import (
    MarketplaceProductList,
    MarketplaceProductDetail,
)

urlpatterns = [
    path("", MarketplaceProductList.as_view(), name="marketplace-product-list"),
    path(
        "/<uuid:uid>",
        MarketplaceProductDetail.as_view(),
        name="marketplace-product-detail",
    ),
]

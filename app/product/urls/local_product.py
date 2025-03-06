from django.urls import path

from product.views.local_product import LocalProductList, LocalProductDetail


urlpatterns = [
    path("", LocalProductList.as_view(), name="local-product-list"),
    path("/<uuid:uid>", LocalProductDetail.as_view(), name="local-product-detail"),
]

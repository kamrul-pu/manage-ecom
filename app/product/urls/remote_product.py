from django.urls import path

from product.views.remote_product import RemoteProductList, RemoteProductDetail


urlpatterns = [
    path("", RemoteProductList.as_view(), name="remote-product-list"),
    path("/<uuid:uid>", RemoteProductDetail.as_view(), name="remote-product-detail"),
]

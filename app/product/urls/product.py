from django.urls import path

from product.views.product import ProductList, ProductDetail


urlpatterns = [
    path("", ProductList.as_view(), name="product-list"),
    path("/<uuid:uid>", ProductDetail.as_view(), name="product-detail"),
]

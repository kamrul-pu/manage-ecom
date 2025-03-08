from django.urls import path, include

urlpatterns = [
    path("", include("product.urls.product"), name="product-urls"),
]

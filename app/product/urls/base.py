from django.urls import path, include

urlpatterns = [
    path("/local", include("product.urls.local_product"), name="local-product-url"),
    path("/remote", include("product.urls.remote_product"), name="remote-product-urls"),
]

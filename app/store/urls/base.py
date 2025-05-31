from django.urls import path, include


urlpatterns = [
    path("", include("store.urls.store"), name="store-urls"),
]

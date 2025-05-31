from django.urls import path

from store.views.store import StoreList, StoreDetail, StoreWareHouseList

urlpatterns = [
    path("", StoreList.as_view(), name="store-list"),
    path("/<uuid:uid>", StoreDetail.as_view(), name="store-detail"),
    path(
        "/<uuid:uid>/warehouses",
        StoreWareHouseList.as_view(),
        name="store-warehouse-list",
    ),
]

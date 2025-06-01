from django.urls import path
from product.views.mapping import MappingList, MappingDetail

urlpatterns = [
    path("", MappingList.as_view(), name="mapping-list"),
    path("/<uuid:uid>", MappingDetail.as_view(), name="mapping-detail"),
]

from django.urls import path

from channel.views.channels import ChannelList, ChannelDetail


urlpatterns = [
    path("", ChannelList.as_view(), name="channel-list"),
    path("/<uuid:uid>", ChannelDetail.as_view(), name="channel-detail"),
]

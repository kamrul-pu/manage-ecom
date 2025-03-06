from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from channel.serializers.channels import ChannelListSerializer, ChannelDetailSerializer

from channel.models import Channel


class ChannelList(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Channel().get_all_actives()
    serializer_class = ChannelListSerializer


class ChannelDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Channel().get_all_actives()
    serializer_class = ChannelDetailSerializer
    lookup_field = "uid"

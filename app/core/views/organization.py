"""Views for Organization."""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)

from core.models import Organization
from core.serializers.organization import (
    OrganizationListSerializer,
    OrganizationDetailSerializer,
)


class OrganizationList(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = OrganizationListSerializer
    queryset = Organization().get_all_actives()


class OrganizationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = OrganizationDetailSerializer
    queryset = Organization().get_all_actives()
    lookup_field = "uid"

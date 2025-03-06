"""Views for Users."""

from django.contrib.auth import get_user_model

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

from core.token_authentication import JWTAuthentication
from core.serializers.user import (
    UserListSerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
    MeSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
)

User = get_user_model()


class UserList(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserListSerializer
    queryset = User().get_all_actives()


class UserDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserDetailSerializer
    queryset = User().get_all_actives()
    lookup_field = "uid"


class UserRegistration(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    queryset = User().get_all_actives()


class MeDetail(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data[
                "user"
            ]  # Get the user object from validated data
            tokens, _ = JWTAuthentication.generate_token_pair(
                user
            )  # Generate both tokens

            # Prepare user data for response
            user_data = {
                "id": str(user.id),
                "uid": str(user.uid),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_kind": user.kind,
            }

            return Response(
                {
                    "message": "Login Success",
                    "tokens": tokens,  # Includes both access_token and refresh_token
                    "user": user_data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token_info = serializer.validated_data["token_info"]
            user = serializer.validated_data["user"]
            user_data = {
                "id": str(user.id),
                "uid": str(user.uid),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_kind": user.kind,
            }
            return Response(
                {
                    "message": "Token Refresh Success",
                    "tokens": token_info,
                    "user": user_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

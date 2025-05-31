"""Serializer for user model."""

from django.contrib.auth import get_user_model, authenticate

from rest_framework import status
from rest_framework import serializers

from core.token_authentication import JWTAuthentication
from core.serializers.organization import OrganizationBase

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "uid",
            "organization",
            "first_name",
            "last_name",
            "email",
            "gender",
            "kind",
            "image",
        )
        read_only_fields = ("id", "uid")


class UserDetailSerializer(UserListSerializer):
    organization = OrganizationBase(read_only=True)

    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields + (
            "status",
            "is_staff",
        )
        read_only_fields = UserListSerializer.Meta.read_only_fields + ()


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Specify password and confirm_password fields as write_only, meaning they won't be included in responses
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},  # Styling to indicate it's a password field
        trim_whitespace=False,
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    # Custom validation for password to check if it matches confirm_password
    def validate_password(self, value):
        password = value
        confirm_password = self.initial_data.get("confirm_password", "")
        if password != confirm_password:
            raise serializers.ValidationError(
                detail="Password and confirm password don't match!!!",  # Error message
                code=status.HTTP_400_BAD_REQUEST,  # HTTP status code
            )
        return value

    class Meta:
        model = User  # Specify the model for the serializer
        fields = (
            "first_name",
            "last_name",
            "phone",
            "email",
            "gender",
            "image",
            "password",
            "confirm_password",
        )  # Fields to include in the serialization

    # Custom create method to handle user creation
    def create(self, validated_data):
        validated_data.pop(
            "confirm_password", None
        )  # Remove confirm_password from validated data
        user = User(**validated_data)  # Create a new user instance with validated data
        user.set_password(validated_data.get("password", ""))  # Set user's password
        user.save()  # Save the user to the database
        return user  # Return the created user instance


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "uid",
            "first_name",
            "last_name",
            "phone",
            "email",
            "gender",
            "image",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "uid",
            "created_at",
            "updated_at",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=255,
        write_only=True,
        style={"input_type": "password"},
    )

    # Read-only fields for response
    id = serializers.IntegerField(read_only=True)
    uid = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    user_kind = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email:
            raise serializers.ValidationError(
                detail="An email address is required for login",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not password:
            raise serializers.ValidationError(
                detail="A password is required for login",
                code=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                detail="Invalid Credentials",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_active:
            raise serializers.ValidationError(
                detail="User is Inactive",
                code=status.HTTP_400_BAD_REQUEST,
            )

        # Return user object instead of just email and id
        return {
            "user": user,  # Pass the full user object
            "email": user.email,
            "id": user.id,
            "uid": user.uid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_kind": user.kind,
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        refresh_token = attrs.get("refresh_token")
        if not refresh_token:
            raise serializers.ValidationError(
                detail="A refresh token is required",
                code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token_info, user = JWTAuthentication.refresh_access_token(refresh_token)
            return {
                "token_info": token_info,
                "user": user,
            }
        except Exception as e:
            raise serializers.ValidationError(
                detail=str(e),
                code=status.HTTP_400_BAD_REQUEST,
            )

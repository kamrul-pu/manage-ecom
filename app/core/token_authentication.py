"""Custom Authentication Class."""

from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import secrets

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Custom authentication class using JSON Web Tokens (JWT) with refresh token support.
    """

    ACCESS_TOKEN_LIFETIME = timedelta(hours=24)
    REFRESH_TOKEN_LIFETIME = timedelta(days=7)

    def authenticate(self, request):
        token = self.extract_token(request)
        if token is None:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.verify_token(payload=payload)  # Still works as an instance method here
            user = User.objects.get(id=payload["id"])
            return (user, None)
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed(detail="Invalid Token", code=400)

    @staticmethod
    def verify_token(payload):
        """
        Verify the JWT token's expiration.

        Args:
            payload (dict): The decoded JWT payload.

        Raises:
            InvalidTokenError: If the token has no expiration timestamp.
            ExpiredSignatureError: If the token has expired.
        """
        if "exp" not in payload:
            raise InvalidTokenError("Token has no expiration")

        exp_timestamp = payload["exp"]
        current_timestamp = datetime.now(timezone.utc).timestamp()
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        auth_header = request.headers.get("Authorization", None)
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    @staticmethod
    def generate_token(user, token_type="access"):
        """
        Generate a JWT token for the given user.

        Args:
            user: User instance
            token_type (str): Type of token to generate ("access" or "refresh")

        Returns:
            tuple: (token, user) - The encoded JWT token and user object
        """
        current_time = datetime.now(timezone.utc)

        payload = {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "user_kind": user.kind,  # Added user.kind to payload
            "iat": current_time.timestamp(),
        }

        if token_type == "access":
            expiration = current_time + JWTAuthentication.ACCESS_TOKEN_LIFETIME
            payload["type"] = "access"
        elif token_type == "refresh":
            expiration = current_time + JWTAuthentication.REFRESH_TOKEN_LIFETIME
            payload["type"] = "refresh"
            payload["jti"] = secrets.token_hex(16)
        else:
            raise ValueError("Invalid token type")

        payload["exp"] = expiration.timestamp()
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token, user

    @staticmethod
    def generate_token_pair(user):
        """
        Generate both access and refresh tokens for a user.

        Args:
            user: User instance

        Returns:
            tuple: (dict of tokens, user)
        """
        access_token, _ = JWTAuthentication.generate_token(user, "access")
        refresh_token, _ = JWTAuthentication.generate_token(user, "refresh")

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_token_expires": int(
                (
                    datetime.now(timezone.utc) + JWTAuthentication.ACCESS_TOKEN_LIFETIME
                ).timestamp()
            ),
            "refresh_token_expires": int(
                (
                    datetime.now(timezone.utc)
                    + JWTAuthentication.REFRESH_TOKEN_LIFETIME
                ).timestamp()
            ),
        }
        return tokens, user

    @staticmethod
    def refresh_access_token(refresh_token):
        """
        Generate a new access token using a valid refresh token.

        Args:
            refresh_token (str): The refresh token to validate

        Returns:
            tuple: (dict of new token info, user)

        Raises:
            AuthenticationFailed: If refresh token is invalid or expired
        """
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
            )

            if payload.get("type") != "refresh":
                raise AuthenticationFailed("Invalid refresh token")

            JWTAuthentication.verify_token(payload)  # Now works as a static method

            user = User.objects.get(id=payload["id"])

            new_access_token, _ = JWTAuthentication.generate_token(user, "access")

            token_info = {
                "access_token": new_access_token,
                "access_token_expires": int(
                    (
                        datetime.now(timezone.utc)
                        + JWTAuthentication.ACCESS_TOKEN_LIFETIME
                    ).timestamp()
                ),
            }
            return token_info, user

        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid or expired refresh token")

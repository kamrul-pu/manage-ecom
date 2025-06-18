from rest_framework import permissions
from rest_framework.permissions import BasePermission
from core.choices import UserKind


class IsAdmin(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind == UserKind.ADMIN

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.organization
            and request.user.organization_id == obj.organization_id
        )


class IsSuperAdmin(BasePermission):
    """
    Custom permission to only allow super admin users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind == UserKind.SUPER_ADMIN


class IsManager(BasePermission):
    """
    Custom permission to only allow manager users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind == UserKind.MANAGER


class IsEmployee(BasePermission):
    """
    Custom permission to only allow employee users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind == UserKind.EMPLOYEE


class IsClient(BasePermission):
    """
    Custom permission to only allow client users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind == UserKind.CLIENT


class IsDeveloper(BasePermission):
    """
    Custom permission to only allow developer users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind == UserKind.DEVELOPER


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Custom permission to allow authenticated users to perform any action,
    while unauthenticated users can only read (GET) data.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Custom permission to allow only authenticated users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsKindDefined(BasePermission):
    """
    Custom permission to check if the user kind is defined.
    """

    def has_permission(self, request, view):
        return request.user and request.user.kind != UserKind.UNDEFINED

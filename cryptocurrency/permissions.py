from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["POST", "PATCH", "PUT", "DELETE"]:
            return request.user and request.user.is_superuser
        return True
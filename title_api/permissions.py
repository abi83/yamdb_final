from rest_framework import permissions


class AuthorPermissions(permissions.BasePermission):
    """Review and Comment object can be edited by object author"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)

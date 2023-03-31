from rest_framework import permissions


class AuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.is_staff
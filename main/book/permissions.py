from rest_framework import permissions
from .models import Author


class IsOwnerOrIsAuthenticatedReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        user = request.user
        return obj.user == user


class IsAuthorOrIsAuthenticatedReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        user = request.user
        author = Author.objects.get(user=user)
        return obj.author == author
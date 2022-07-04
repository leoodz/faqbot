from rest_framework.permissions import BasePermission


class Authent(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and obj.author==request.user
        )
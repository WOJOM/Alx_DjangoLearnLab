from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Safe methods allowed to everyone. Write methods only allowed to object owner or staff.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return getattr(obj, 'author', None) == request.user

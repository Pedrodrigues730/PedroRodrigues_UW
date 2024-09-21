from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only administrators to perform write operations (create, update, delete).
    Anonymous users are limited to read-only access.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.
        :param request: The incoming request object.
        :param view: The view where the request is being processed.
        :return: True if the user is an admin or is performing a read operation, otherwise False.
        """
        if request.method in permissions.SAFE_METHODS:
            # Allow GET, HEAD, and OPTIONS requests for everyone
            return True
        # Only allow admins to perform unsafe actions (POST, PUT, DELETE)
        return request.user and request.user.is_staff

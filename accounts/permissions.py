from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission to only allow owners or admins to access/edit objects.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Check if object is a User instance
        if hasattr(obj, 'id'):
            # Allow access if user is owner or admin
            return obj.id == request.user.id or request.user.is_staff
            
        return False
from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _

class TicketPermission(BasePermission):
    """
    Ticket object-level permission:
    - All authenticated users can create tickets
    - Owners can read/update their own tickets
    - Admins/Agents have full access to all tickets
    - Unauthenticated users have no access
    """
    
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated
        return True  # List/retrieve handled by object permissions

    def has_object_permission(self, request, view, obj):
        # Unauthenticated users
        if not request.user.is_authenticated:
            return False
            
        # Admins/Agents have full access
        if request.user.is_staff or request.user.is_agent:
            return True
            
        # Users can only access their own tickets
        return obj.user == request.user